from typing import Optional,List
import pinecone,re
import os
import uuid
import numpy as np
import logging
from pydantic import Field

from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.load.serializable import Serializable
from autoxx.utils.processing_text import split_text
from langchain.chains import HypotheticalDocumentEmbedder
from autoxx.tools.knowledge_base.prompts import load_prompt
from langchain.schema import HumanMessage, SystemMessage, AIMessage, BaseMessage
logger = logging.getLogger(__name__)

class Document(Serializable):
    text: str
    doc_id: str = None
    extra_info: dict = Field(default_factory=dict)
    score: float = None

class knowleage_application:
    def __init__(self, corpus:str, namespace:Optional[str] = None, model:str = "gpt-3.5-turbo-16k", embedding_model: str="text-embedding-ada-002"):
        if not is_valid_corpus_name(corpus):
            raise ValueError(f"Invalid corpus name: {corpus}. coprus name must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character")
        
        self.corpus = corpus
        self.namespace=namespace
        self._text_key = "text"

        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        assert pinecone_api_key is not None, "Please set PINECONE_API_KEY environment variable"
        pinecone_environment =  os.getenv("PINECONE_ENVIRONMENT") or "us-central1-gcp"

        pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
        index_list = pinecone.list_indexes()
        if self.corpus not in index_list:
            logger.info(f"vector index {self.corpus} not found, creating...")
            pinecone.create_index(name=self.corpus, metric="cosine", dimension=1536)
        self.pinecone_index = pinecone.Index(self.corpus)

        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.llm = ChatLLM(model_name=model)
        self.hyde_embeddings = HypotheticalDocumentEmbedder.from_llm(self.llm, self.embeddings, "web_search")
        self.vectorstore = Pinecone(self.pinecone_index, self.embeddings.embed_query, self._text_key, self.namespace)
        self.hyde_vectorstore = Pinecone(self.pinecone_index, self.hyde_embeddings.embed_query, self._text_key, self.namespace)


    def query(self, query:str, enable_hype:bool = True, chat_history: Optional[list[dict[str, str]]]=None):
        """
        chat_history: list of dict, each dict has two keys: "role" (ai, human, system) and "content"
        """
        docs = self.similarity_search(query, enable_hype)

        system_prompt = load_prompt("qa")
        for index, doc in enumerate(docs):
            system_prompt += f"Document_{index}: {doc.text}\n\n"

        messages = [
            SystemMessage(content=system_prompt),
        ]

        if chat_history is not None and len(chat_history) > 0:
            messages.extend(messages_from_dict(chat_history))

        messages.append(HumanMessage(content=query))
        
        answer = self.llm(messages).content

        return {"answer": answer, "reference": docs}

    def similarity_search(self, query:str, enable_hype:bool = True, retrieve_top_k:int = 3):
        res = []
        if enable_hype:
            docs = self.hyde_vectorstore.similarity_search_with_score(query, retrieve_top_k)
        else:
            docs = self.vectorstore.similarity_search_with_score(query, retrieve_top_k)

        for doc, score in docs:
            res.append(Document(
                doc_id= doc.metadata["doc_id"] if "doc_id" in doc.metadata else None,
                text=doc.page_content,
                extra_info=doc.metadata,
                score=score
            ))
        return res

    def upsert_document(self, docs: List[Document]) -> List[str]:
        texts = []
        medadatas = []
        ids = []
        for doc in docs:
            doc.doc_id = doc.doc_id or str(uuid.uuid4())
            # chunks = [chunk for chunk, _ in (split_text(doc.text))]
            texts.append(doc.text)
            medadatas.append(doc.extra_info)
            ids.append(doc.doc_id)

        return self.vectorstore.add_texts(texts, medadatas, ids=ids, namespace=self.namespace)

    def delete_document(self, document_ids: Optional[List[str]] = None) -> None:
        if document_ids is not None and len(document_ids) > 0:
            self.vectorstore.delete(
                ids=document_ids,
            )
        
        """
        if doc_ids is not None and len(doc_ids) > 0:
            self.pinecone_index.delete(
                filter={"doc_id": {"$in": document_ids}},
                namespace=self.namespace,
            )
        """

    def retrieve_document(self, document_ids: Optional[List[str]] = None) ->  List[Document]:
        docs = []
        # use fetch api to fecth specific documents
        if document_ids is not None and len(document_ids) > 0:
            response =  self.pinecone_index.fetch(ids=document_ids, namespace=self.namespace)
            for id, vector in response['vectors'].items():
                metadata = vector['metadata']
                if self._text_key in metadata:
                    text = metadata.pop(self._text_key)
                    docs.append(Document(doc_id=id, text=text, extra_info=metadata))
                else:
                    logger.warning(
                        f"Found document with no `{self._text_key}` key. Skipping."
                    )
            return docs

        filter = None
        """
        if internal_kb_ids is not None and len(internal_kb_ids) > 0:
            filter={self._kb_id_key: {"$in": internal_kb_ids}}
        """

        # try to load all documents in the index   
        index_description = self.pinecone_index.describe_index_stats()
        vector_count = index_description["total_vector_count"]
        if self.namespace in index_description["namespaces"]:
            vector_count = index_description["namespaces"][self.namespace]["vector_count"]

        logger.info(f"retrieving in namespace {self.namespace}, vector count: {vector_count}")
        if vector_count == 0:
            return docs
    
        response = self.pinecone_index.query(
            top_k=vector_count,
            vector=list(np.zeros(1536)),
            namespace=self.namespace,
            fikter=filter,
            include_metadata=True,
        )

        for res in response["matches"]:
            metadata = res["metadata"]
            id = res["id"]
            if self._text_key in metadata:
                text = metadata.pop(self._text_key)
                docs.append(Document(doc_id=id, text=text, extra_info=metadata))
            else:
                logger.warning(
                    f"Found document with no `{self._text_key}` key. Skipping."
                )
        return docs

def is_valid_corpus_name(corpus_name):
    # Regular expression pattern for the corpus name rule
    pattern = r'^[a-z0-9][a-z0-9-]*[a-z0-9]$'

    # Check if the corpus name matches the pattern
    if re.match(pattern, corpus_name):
        return True
    else:
        return False
    
def ChatLLM(
    model_name="gpt-3.5-turbo",
    temperature=0,
    request_timeout=120,
):
    if model_name.startswith("gpt-4") and os.getenv("GPT_4_MODEL_API_KEY") is not None:
        return ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
            model_kwargs={
                "api_key": os.getenv("GPT_4_MODEL_API_KEY"),
                "api_base": os.getenv("GPT_4_MODEL_API_BASE", "https://api.openai.com/v1"),
                "api_type": os.getenv("GPT_4_MODEL_API_TYPE", "open_ai"),
                "api_version": os.getenv("GPT_4_MODEL_API_VERSION"),
                "deployment_id": os.getenv("GPT_4_MODEL_API_DEPLOYMENT_ID"),
            }
        )
    else:
        return ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
        )

def _message_from_dict(message: dict) -> BaseMessage:
    _type = message["role"]
    if _type == "human":
        return HumanMessage(message["content"])
    elif _type == "ai":
        return AIMessage(**message["content"])
    elif _type == "system":
        return SystemMessage(**message["content"])
    else:
        raise ValueError(f"Got unexpected type: {_type}")


def messages_from_dict(messages: List[dict]) -> List[BaseMessage]:
    """Convert messages from dict.

    Args:
        messages: List of messages (dicts) to convert.

    Returns:
        List of messages (BaseMessages).
    """
    return [_message_from_dict(m) for m in messages]
