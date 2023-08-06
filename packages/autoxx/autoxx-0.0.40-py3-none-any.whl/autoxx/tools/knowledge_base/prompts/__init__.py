import os
import inspect


def load_prompt(prompt):
    file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
    dir_path = os.path.dirname(file_path)
    path = f"{dir_path}/{prompt}"
    with open(path, "r") as f:
        return f.read()