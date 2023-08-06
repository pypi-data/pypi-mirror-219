import os
from pathlib import Path


def read(path: str):
    with open(path, encoding="utf-8") as file:
        return file.read()


def write(path: str, data):
    with open(path, mode='w+') as file:
        return file.write(data)


def append(path: str, data):
    with open(path, mode='a+') as file:
        return file.write(data)


def resolve(*path_tokens):
    return Path(os.path.join(*path_tokens)).__str__()
