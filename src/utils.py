import json
import os
import pickle
import re
import sys
from enum import Enum
from time import sleep
from random import random
from contextlib import contextmanager
from typing import Optional, Dict
from urllib.request import urlopen

from collections import defaultdict

# class strEnum(Enum):
#     def __str__(self):
#         return str(self.value)
from KdamClasses import Faculty

"""
Paths and other string constants
"""


class Semester(Enum):
    Semester = "01"
    Year = "2018"
    TestYear = str(int(Year) + int(Semester) - 1)  # For the regex searching for exam dates


class Addresses(Enum):
    TechnionUg = "https://ug3.technion.ac.il/rishum/course?SEM=" + Semester.Year.value + Semester.Semester.value + "&MK="
    TechnionGrad = "http://www.graduate.technion.ac.il/heb/Subjects/?Sub="


class Paths(Enum):
    # TODO: use os.path.join on these
    MainPath = os.path.abspath("..")
    dataPath = MainPath + r"\data"
    pdfPath = dataPath + r"\pdf"
    txtPath = dataPath + r"\txt"
    htmlPath = dataPath + r"\html"
    jsonPath = dataPath + r"\json"
    picklePath = dataPath + r"\pickle"


courseRegex = "(?:^|\D)(\d{5,6})(?:\D|$)"

# MyDataPath = r"C:\Users\ADMIN\PycharmProjects\Project_Kdam\html"

"""
For PDF and TXT parsers
"""


class FilenameConsts(Enum):
    FileName = "blah-"
    Suffix = ".txt"


"""
Dictionary class
"""


# TODO: use this for Faculties and Courses
class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


# d = keydefaultdict(C)
# d[x] # returns C(x)

"""
Generic functions
"""


def printInLines(Iterable, file=None):
    print('\n'.join(str(x) for x in Iterable), file=file)


def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


@contextmanager
def tempOpen(path, mode, encoding: Optional[str] = None):
    """
    Attempts to open the file in the path with mode and encoding, at the end closes and deletes the file
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


def randomSleep():
    if random() > 0.7:
        sleep(5)


def fileExists(filename):
    # b1 = os.path.exists(filename)
    # b2 = os.path.isfile(filename)
    # if (b1 and b2): return True
    # return False
    return ((os.path.exists(filename)) and (os.path.isfile(filename)))


def courseExists(courseId):
    return fileExists(htmlPath + "\\" + str(courseId) + ".htm")


"""
Data storage utilities - pickle and JSON
"""


def toJSON(object):
    return json.dumps(object, default=lambda x: x.__dict__)


def toJSONFile(object, filename: str, indent=None):
    with open(filename, 'w+', encoding='utf8') as file:
        json.dump(object, file, default=lambda x: x.__dict__, ensure_ascii=False, indent=indent)


def toPickle(object, filename: str):
    with open(filename, 'wb+') as file:
        pickle.dump(object, file, protocol=pickle.HIGHEST_PROTOCOL)


def fromPickle(filename):
    with open(filename, 'rb') as file:
        result = pickle.load(file, encoding='utf8')
    return result
