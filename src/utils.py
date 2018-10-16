import json
import os
import pickle
import sys
from collections import defaultdict
from contextlib import contextmanager
from typing import Optional, Iterable

# Course Regex


course_regex = "(?:^|\D)(\d{5,6})(?:\D|$)"
bad_course_on_grad = "z/OS (CICS)"

# Paths and other string constants


class Semester:
    Semester = "01"
    Year = "2018"
    # TestYear = str(int(Year) + int(Semester) - 1)


class Addresses:
    TechnionUg = "https://ug3.technion.ac.il/rishum/course?SEM=" + Semester.Year + Semester.Semester + "&MK="
    TechnionGrad = "http://www.graduate.technion.ac.il/heb/Subjects/?Sub="


class Paths:
    mainPath = os.path.abspath("..")
    dataPath = os.path.join(mainPath, "data")
    pdfPath = os.path.join(dataPath, "pdf")

    txtPath = os.path.join(dataPath, "txt")
    bad_online_courses = os.path.join(txtPath, "badOnlineCourses.txt")
    bad_catalogue_courses = os.path.join(txtPath, "badCatalogueCourses.txt")

    testPath = os.path.join(dataPath, "tests")
    htmlPath = os.path.join(dataPath, "html")

    jsonPath = os.path.join(dataPath, "json")
    jsonTests = os.path.join(jsonPath, "tests.json")
    jsonNewCourses = os.path.join(jsonPath, "coursesUpdated.json")

    picklePath = os.path.join(dataPath, "pickle")
    pickleFaculties = os.path.join(picklePath, "faculties.p")
    pickleCourses = os.path.join(picklePath, "courses.p")
    pickleNewFaculties = os.path.join(picklePath, "facultiesUpdated.p")
    pickleNewCourses = os.path.join(picklePath, "coursesUpdated.p")


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

def dict_recursive_format(dictionary: dict) -> dict:
    """
    returns a new dictionary where all non-string keys and values have been (recursively) turned into strings.
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


# Generic functions


def print_in_lines(iterable: Iterable, file=None):
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
