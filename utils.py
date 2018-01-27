import json
import os
import pickle
import re
import sys
from time import sleep
from random import random
from contextlib import contextmanager
from urllib.request import urlopen

"""
Paths and other string constants
"""

Semester = "02"
Year = "2017"
TestYear = str(int(Year) + int(Semester) - 1)  # For the regex searching for exam dates

TechnionUg = "https://ug3.technion.ac.il/rishum/course?SEM=" + Year + Semester + "&MK="
TechnionGrad = "http://www.graduate.technion.ac.il/heb/Subjects/?Sub="

MainPath = r"C:\Users\ADMIN\PycharmProjects\Project_Kdam"
data1Path = MainPath + r"\data1"
htmlPath = MainPath + r"\html"
jsonPath = data1Path + "\json"
picklePath = data1Path + "\pickle"

courseRegex = "(?:^|\D)(\d{5,6})(?:\D|$)"

# MyDataPath = r"C:\Users\ADMIN\PycharmProjects\Project_Kdam\html"

"""
Generic functions
"""


def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


@contextmanager
def tempOpen(path, mode, encoding):
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


def toJSONFile(object, filename):
    with open(filename, 'w+', encoding='utf8') as file:
        json.dump(object, file, default=lambda x: x.__dict__)


def toPickle(object, filename):
    with open(filename, 'wb+') as file:
        pickle.dump(object, file, protocol=pickle.HIGHEST_PROTOCOL)


def fromPickle(filename):
    with open(filename, 'rb') as file:
        result = pickle.load(file, encoding='utf8')
    return result
