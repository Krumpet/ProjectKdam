import re
from courseDownloader import getHTMLDataFromCourse, getHTMLDataFromGrad
from utils import *
from KdamClasses import *

htmlPath2 = htmlPath + "2"

# with open(htmlPath + r"\648013.htm", encoding='utf8') as course:
#     data = course.read()
#     match = re.findall("לא קיים", data)
#     print("matches: ", match)
#
# with open(htmlPath + r"\106353.htm", encoding='utf8') as course:
#     data = course.read()
#     match = re.findall("לא קיים", data)
#     print("matches: ", match)

testCourses = ["648013", "106353"]

Courses: Dict[CourseNum, Course] = fromPickle(picklePath + "\\Courses.txt")


def getCodec(data):
    """
    receives byes of data from opening HTML file,
    returns the appropriate codec i.e 'utf-8' or 'windows-1255'
    :param data:
    :return:
    """
    return re.findall(r"(?i)charset=\"?([^\s]+)\"", str(data))[0]


def downloadCourse(courseId):
    data = getHTMLDataFromCourse(courseId)
    # check if this course exists in UG:
    if (len(re.findall("לא קיים", str(data, encoding='utf8'))) > 0):
        print("going to grad instead")
        data = getHTMLDataFromGrad(courseId)
    # print(str(data))
    # charset = getCodec(data)
    # print(charset)
    open(htmlPath2 + "\\" + str(courseId) + ".htm", "wb").write(data)


def getKdams(data):
    try:
        kdams = list(set(re.findall("\d{5,6}", re.findall("מקצועות קדם.*?/div><div", data, re.DOTALL)[0])))
    except:
        kdams = []
    return kdams


def getZamuds(data):
    try:
        zamuds = list(set(re.findall("\d{5,6}", re.findall("מקצועות צמודים.*?/div><div", data, re.DOTALL)[0])))
    except:
        zamuds = []
    return zamuds


def getSubject(data):
    try:
        subject = re.findall("\|.*\|(.*)</title>", data)[0].strip()
        # print("subject is " + subject)
    except:
        subject = "None"
    return subject


def getExams(data):
    try:
        exams = re.findall(">.*(\d\d\.\d\d).*2018", data)[:2]
    except:
        exams = "None"
    return exams


# def getKdamArrayAndZamudArray(courseId):
#     data = open(htmlPath2 + "\\" + str(courseId) + ".htm", encoding="utf8").read()
#
#     subject = getSubject(data)
#
#     kdams = getKdams(data)
#
#     zamuds = getZamuds(data)
#
#     return [subject, kdams, zamuds]


def getCourseInfo(courseId):
    with tempOpen(htmlPath2 + "\\" + str(courseId) + ".htm", mode='rb', encoding=None) as file:
        byteData = file.read()
        encoding = getCodec(byteData)
        strData = str(byteData, encoding=encoding)
        Courses[courseId].name = getSubject(strData)
        Courses[courseId].kdams = getKdams(strData)
        Courses[courseId].zamuds = getZamuds(strData)
        Courses[courseId].moed_A, Courses[courseId].moed_B = getExams(strData)


# try:
#     print(str(data, encoding='utf-8'))
# except:
#     print(str(data, encoding='windows-1255'))
# subject = getSubject(data)
# kdams = getKdams(data)
# zamuds = getZamuds(data)

# return [subject, kdams, zamuds]
# with tempOpen(htmlPath2 + "\\" + "106353" + ".htm", mode='rb', encoding=None) as file:

# with open(htmlPath2 + "\\" + "106353" + ".htm", mode='rb') as file:
#     byteData = file.read()
#     strData = str(byteData, encoding='utf8')
#     print(strData)
#
# with open(htmlPath2 + "\\" + "648013" + ".htm", mode='r', encoding='utf8', errors='ignore') as file:
#     strData = file.read()
#     print(strData)
#
# with open(htmlPath2 + "\\" + "648013" + ".htm", mode='r', encoding='windows-1255', errors='ignore') as file:
#     strData = file.read()
#     print(strData)

# for course in testCourses:
# print(getKdamArrayAndZamudArray("106353"))
# print(getKdamArrayAndZamudArray("648013"))

for course in testCourses:
    try:
        getCourseInfo(course)
    except:
        continue

print(Courses[testCourses[0]])
print(Courses[testCourses[1]])

# downloadCourse(testCourses[0])

# downloadAllCourses(testCourses)
