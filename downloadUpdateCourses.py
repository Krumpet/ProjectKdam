import re
# from courseDownloader import getHTMLDataFromCourse, getHTMLDataFromGrad
from utils import *
from KdamClasses import *

Faculties: Dict[str, Faculty] = fromPickle(picklePath + "\\faculties.txt")
Courses: Dict[CourseNum, Course] = fromPickle(picklePath + "\\courses.txt")


def getEncoding(data):
    """
    receives byes of data from opening HTML file,
    returns the appropriate codec i.e 'utf-8' or 'windows-1255'
    :param data:
    :return:
    """
    return re.findall(r"(?i)charset=\"?([^\s]+)\"", str(data))[0]


def getHtmlDataFromURL(url):
    f = urlopen(url)
    return f.read()


def getHTMLDataFromCourse(courseId):
    return getHtmlDataFromURL(TechnionUg + str(courseId))


def getHTMLDataFromGrad(courseId):
    return getHtmlDataFromURL(TechnionGrad + str(courseId))


def downloadCourse(courseId):
    if (False == courseExists(courseId)):
        data = getHTMLDataFromCourse(courseId)
        # check if this course exists in UG:
        if (len(re.findall("לא קיים", str(data, encoding='utf8'))) > 0):
            data = getHTMLDataFromGrad(courseId)
        open(htmlPath + "\\" + str(courseId) + ".htm", "wb").write(data)
        randomSleep()


def getKdams(data):
    try:
        kdams = list(set(re.findall(courseRegex, re.findall("מקצועות קדם.*?/div><div", data, re.DOTALL)[0])))
        kdams = list(set([CourseNum(x).id for x in kdams]))
    except:
        kdams = []
    return kdams


def getZamuds(data):
    try:
        zamuds = list(set(re.findall(courseRegex, re.findall("מקצועות צמודים.*?/div><div", data, re.DOTALL)[0])))
        zamuds = list(set([CourseNum(x).id for x in zamuds]))
    except:
        zamuds = []
    return zamuds


def getSubject(data):
    try:
        subject = re.findall("\|.*\|(.*)</title>", data)[0].strip()
    except:
        subject = "None"
    return subject


def getExams(data):
    exams = re.findall(">.*(\d\d\.\d\d).*" + TestYear, data)

    if (len(exams) > 1):
        return exams[:2]
    elif (len(exams) == 1):
        return exams[0], "None"
    else:
        return "None", "None"


def getCourseInfo(courseId):
    path = htmlPath + "\\" + str(courseId) + ".htm"
    try:
        with open(path, mode='r', encoding='utf8') as file:
            strData = file.read()
            Courses[courseId].name = getSubject(strData)
            Courses[courseId].kdams = getKdams(strData)
            Courses[courseId].zamuds = getZamuds(strData)
            Courses[courseId].moed_A, Courses[courseId].moed_B = getExams(strData)
    except UnicodeDecodeError:
        with open(path, mode='r', encoding='windows-1255') as file:
            strData = file.read()
            htmlParser = MyHTMLParser()
            htmlParser.feed(strData)
            Courses[courseId].name = htmlParser.name
    finally:
        os.remove(path)


def updateFollowups():
    for courseId, course in Courses.items():
        for kdam in course.kdams:
            if kdam in Courses.keys():
                Courses[kdam].followups.append(courseId)


for course in Courses.keys():
    downloadCourse(course)

for course in Courses:
    getCourseInfo(course)

updateFollowups()

toPickle(Courses, picklePath + r"\courses.txt")
