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


# class Semester(Enum):
#     Semester = "01"
#     Year = "2018"
#     TestYear = str(int(Year) + int(Semester) - 1)  # For the regex searching for exam dates

class Semester:
    Semester = "01"
    Year = "2018"
    # TestYear = str(int(Year) + int(Semester) - 1)


class Addresses:
    TechnionUg = "https://ug3.technion.ac.il/rishum/course?SEM=" + Semester.Year + Semester.Semester + "&MK="
    TechnionGrad = "http://www.graduate.technion.ac.il/heb/Subjects/?Sub="


class Paths:
    # TODO: use os.path.join on these
    mainPath = os.path.abspath("..")
    dataPath = os.path.join(mainPath, "data")
    pdfPath = os.path.join(mainPath, "pdf")
    txtPath = os.path.join(mainPath, "txt")
    testPath = os.path.join(mainPath, "tests")
    htmlPath = os.path.join(mainPath, "html")

    jsonPath = os.path.join(mainPath, "json")
    jsonTests = os.path.join(jsonPath, "tests.json")
    jsonNewCourses = os.path.join(jsonPath, "coursesUpdated.json")

    picklePath = os.path.join(mainPath, "pickle")
    pickleFaculties = os.path.join(picklePath, "faculties.p")
    pickleCourses = os.path.join(picklePath, "courses.p")
    pickleNewFaculties = os.path.join(picklePath, "facultiesUpdated.p")
    pickleNewCourses = os.path.join(picklePath, "coursesUpdated.p")


courseRegex = "(?:^|\D)(\d{5,6})(?:\D|$)"

# MyDataPath = r"C:\Users\ADMIN\PycharmProjects\Project_Kdam\html"

"""
For PDF and TXT parsers
"""

# class FilenameConsts(Enum):
#     # todo this should actually be an argument to txtParser
#     FileName = "blah-"
#     Suffix = ".txt"


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

def dictRecursiveFormat(d: dict) -> dict:
    """
    returns a new dictionary where all non-string keys and values have been (recursively) turned into strings.
    Use this for e.g. JSON dumps
    :param d:
    :return:
    """
    newDict = {}
    for key, val in d.items():
        newVal = val if type(val) is not dict else dictRecursiveFormat(val)
        if not isinstance(key, str):
            newDict[str(key)] = newVal
    return newDict


"""
Generic functions
"""


def printInLines(iterable, file=None):
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
    return fileExists(os.path.join(Paths.htmlPath, str(courseId) + ".htm"))


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
