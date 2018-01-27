import json
import re
from urllib.request import urlopen
from typing import Dict
from KdamClasses import Faculty, Course, CourseNum
from utils import *

# numOfPages = 668

# args = [
#     "gs".encode('utf-8'),
#     "-sDEVICE=txtwrite".encode('utf-8'),
#     "-o".encode('utf-8') + "C:\\Users\\ADMIN\\PycharmProjects\\Project_Kdam\\data1\\blah-%d.txt".encode('utf-8'),
#     "C:\\Users\\ADMIN\\PycharmProjects\\Project_Kdam\\data1\\Catalogue17-18.pdf".encode('utf-8')
# ]
#
# ghostscript.Ghostscript(*args)

"""
Parse the entire catalogue into text files (one for each page) using GhostScript:
./gswin64c.exe -sDEVICE=txtwrite
    -o "<Path to keep all text files>\\<some name>-%d.txt"
    "<Path to pdf>\<pdf name>.pdf"
    
    Note the %d which means each page becomes a different txt file
"""

"""
These are the names I gave my text files, and i will be the page number, in range (1,668) because that's
how many pages there were
TODO: export file names and path from the pdfParser file
"""

FileName = "blah-"
Suffix = ".txt"

Faculties: Dict[str, Faculty] = {}
Courses: Dict[CourseNum, Course] = {}


def parseTexts():
    from pdfParser import numOfPages
    for i in range(1, numOfPages + 1):
        # tempOpen closes and deletes the text file after use
        with tempOpen(data1Path + "\\" + FileName + str(i) + Suffix, 'r', encoding="utf8") as file:
            try:
                data = [" ".join(line.split()).strip() for line in file.readlines()]
                if re.search("תו?כנית לימודים", data[0][::-1], re.DOTALL) is None:
                    continue
                """
                The title of pages that contain class lists for each faculty have the format:
                2017/2018 Blah blah blah / 23 Computer Science
                So we capture the '23' and the 'Computer Science'
                """
                facultyCode, facultyName = re.findall("\d+.\d+ +.* +/ +(\d+) +(.*)", data[0])[0]
                # Faculty name is captured in reverse so flip it
                facultyName = facultyName[::-1]
                # TODO: maybe combine data from lines to one big string?
                # This regex captures all 5,6 digit sequences that aren't part of a longer sequence, like phone numbers
                courseInEachLine = [re.findall(courseRegex, data[j]) for j in range(len(data))]
                coursesOnThisPage = list(
                    set([CourseNum(courseNum) for sublist in courseInEachLine for courseNum in sublist]))
                courseObjects = [Courses.get(courseId, Course(courseId)) for courseId in coursesOnThisPage]
                for course in courseObjects:
                    if course.courseId not in Courses.keys():
                        Courses[course.courseId] = course
                if facultyCode not in Faculties.keys():
                    Faculties[facultyCode] = Faculty(facultyCode, facultyName)
                Faculties[facultyCode].addCourses(coursesOnThisPage)

                print("reading page {0}, faculty {1}, faculty code {2}".format(i, facultyName, facultyCode))
            except Exception as e:
                print(e)
                continue


# prune faculties with no courses on their page
def pruneFaculties():
    for k in list(Faculties.keys()):
        if len(Faculties[k].courses) == 0:
            Faculties.pop(k, None)


def writeToFiles():
    toJSONFile(Faculties, jsonPath + "\\faculties.txt")
    toJSONFile(Courses, jsonPath + "\\courses.txt")
    toPickle(Faculties, picklePath + "\\faculties.txt")
    toPickle(Courses, picklePath + "\\courses.txt")


if __name__ == "__main__":
    parseTexts()
    pruneFaculties()
    writeToFiles()

# print(sorted(Courses.keys()))
# print(Faculties.keys())

# for k, v in Faculties.items():
#     print(k, v.courses)

# for k, v in Courses.items():
#     print(k)

# print(len(Courses.keys()))
#
# print(len(list(set(Courses.keys()))))
#
# totalcourse = []
#
# for k, v in Faculties.items():
#     totalcourse.extend(v.courses)
#
# totalcourse = list(set(totalcourse))
# print(len(totalcourse))

# print(Faculties["23"].courses)
#
# print(json.dumps(Courses, default=lambda x: x.__dict__))
#
# data = open(FilePath+"\\"+FileName, "r", encoding="utf8").read()
# data = open(r"C:\Users\ADMIN\PycharmProjects\Project_Kdam\data1\AllFacs.txt", "r").read()
# # print(data)
# pattern = r"חלק ' ד.*חלק ה"
# pattern2 = "TAG_START.*TAG_END"
# segment = re.findall(pattern2, data, re.DOTALL)
# print('\n'.join(segment))
# print(segment.string)
# print(len(segment))
# segment0 = segment[0]
#
# print(segment)
