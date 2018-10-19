import json
import os
import pickle
import sys
from collections import defaultdict
from contextlib import contextmanager
from typing import Optional, Collection


# Dictionary class


# TODO: use this for Faculties and Courses
class KeyDefaultDict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


# d = keydefaultdict(C)
# d[x] # returns C(x)


# Generic functions

def dict_recursive_format(dictionary: dict) -> dict:
    """
    returns a new dictionary where all non-string keys and values have been (recursively)
    turned into strings.
    Use this for e.g. JSON dumps
    :param dictionary:
    :return:
    """
    new_dict = {}
    for key, val in dictionary.items():
        new_val = val if not isinstance(val, dict) else dict_recursive_format(val)
        # if not isinstance(key, str):
        new_dict[str(key)] = new_val
    return new_dict


def print_in_lines(iterable: Collection, file=None):
    print('\n'.join(str(x) for x in iterable), file=file)


def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


@contextmanager
def temp_open(path, mode, encoding: Optional[str] = None):
    """
    Attempts to open the file in the path with mode and encoding,
    at the end closes and deletes the file
    :param path:
    :param mode:
    :param encoding:
    :return:
    """
    # if this fails there is nothing left to do anyways
    file = open(path, mode, encoding=encoding)

    try:
        yield file
    finally:
        file.close()
        os.remove(path)


# Data storage utilities - pickle and JSON


def to_json(obj):
    return json.dumps(obj, default=lambda x: x.__dict__)


def to_json_file(obj, filename: str, indent=None):
    with open(filename, 'w+', encoding='utf8') as file:
        json.dump(obj, file, default=lambda x: x.__dict__, ensure_ascii=False, indent=indent)


def to_pickle(obj, filename: str):
    with open(filename, 'wb+') as file:
        pickle.dump(obj, file, protocol=pickle.HIGHEST_PROTOCOL)


def from_pickle(filename):
    with open(filename, 'rb') as file:
        result = pickle.load(file, encoding='utf8')
    return result

# def randomSleep():
#     if random() > 0.7:
#         sleep(5)


# def fileExists(filename):
#     # b1 = os.path.exists(filename)
#     # b2 = os.path.isfile(filename)
#     # if (b1 and b2): return True
#     # return False
#     return (os.path.exists(filename)) and (os.path.isfile(filename))


# def course_exists(course_id):
#     return fileExists(os.path.join(Paths.htmlPath, str(course_id) + ".htm"))
