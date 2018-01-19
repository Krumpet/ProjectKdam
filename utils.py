import json
import os

import sys


def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def toJSON(object):
    return json.dumps(object, default=lambda x: x.__dict__)


from contextlib import contextmanager


@contextmanager
def tempOpen(path, mode, encoding):
    # if this fails there is nothing left to do anyways
    file = open(path, mode, encoding=encoding)

    try:
        yield file
    finally:
        file.close()
        os.remove(path)
