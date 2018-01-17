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
