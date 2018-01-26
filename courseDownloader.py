from typing import Dict
# from Course import Course
# from Faculty import Faculty
from KdamClasses import *
from utils import *
from txtParser import jsonPath, picklePath
import re

# with open(jsonPath+"\\Faculties.txt", 'r', encoding='utf8') as file:
# Faculties = json.load(file)

# Faculties : Dict[str,Faculty] = fromPickle(picklePath+"\\Faculties.txt")
Courses: Dict[CourseNum, Course] = fromPickle(picklePath + "\\Courses.txt")

# print(Faculties["04"].name)
# print(Courses[CourseNum("234123")].courseId)

"""
For downloading courses
"""


def fileExists(filename):
    return ((os.path.exists(filename)) and (os.path.isfile(filename)))


def courseExists(courseId):
    return fileExists(htmlPath + "\\" + str(courseId) + ".htm")


def getHtmlDataFromURL(url):
    f = urlopen(url)
    return f.read()


def getHTMLDataFromCourse(courseId):
    return getHtmlDataFromURL(TechnionUg + str(courseId))


def getHTMLDataFromGrad(courseId):
    return getHtmlDataFromURL(TechnionGrad + str(courseId))


def downloadCourse(courseId):
    data = getHTMLDataFromCourse(courseId)
    # # check if this course exists in UG:
    # if (len(re.findall("לא קיים", data)) > 0):
    #     data = getHTMLDataFromGrad(courseId)
    open(htmlPath + "\\" + str(courseId) + ".htm", "wb").write(data)


# TODO: Identify "no such course" in UG and get data from graduate
def downloadAllCourses(coursesArray):
    """
    Downloads html files into html data path
    :param coursesArray:
    :return:
    """
    array = coursesArray
    for i in array:
        if (False == courseExists(i)):
            downloadCourse(i)
            randomSleep()


if __name__ == "__main__":
    downloadAllCourses(Courses.keys())

# omg : Dict[str, Course] = {}
# zomg : Dict[str, Faculty] = {}
#
# Fac1 = Faculty("1","Fac1")
# Cour1 = Course("12","cour1")
# Cour1.kdams.append("123")
# print(Cour1.kdams)
# omg["a"] = Cour1
#
# Cour2 = omg["a"]
# Cour2.kdams.append("321")
# print(Cour1.kdams)
# print(Cour2.kdams)
# omg["a"] = Cour2
#
# Fac1.courses["b"] = Cour1
#
# Cour3 = Fac1.courses["b"]
# Cour3.kdams.append("444")
# print(Cour1.kdams)
# print(Cour2.kdams)
# print(Cour3.kdams)
