import re
# from courseDownloader import getHTMLDataFromCourse, getHTMLDataFromGrad
from collections import OrderedDict
import urllib.request as request
from typing import Set, Dict

from utils import *
from KdamClasses import *
from GraduateParser import parseGraduate
from typing import Set

hebrew = ['שם מקצוע', 'מספר מקצוע', 'אתר הקורס', 'נקודות',
          'הרצאה', 'תרגיל', 'מעבדה', 'סמינר/פרויקט', 'סילבוס', 'מקצועות זהים', 'מקצועות קדם', 'מקצועות צמודים',
          'מקצועות ללא זיכוי נוסף', 'מקצועות ללא זיכוי נוסף (מכילים)', 'מקצועות ללא זיכוי נוסף (מוכלים)',
          'עבור לסמסטר', 'אחראים', 'הערות', 'מועד הבחינה', 'מועד א', 'מועד ב', 'מיקום']
irrelevant = 'move_to_semester in_charge comments exam_date exam_A exam_B location'.split()
english = 'name id site points lecture tutorial lab project syllabus identical kdam adjacent no_more no_more_contains no_more_included'.split() + irrelevant
trans = dict(zip(hebrew, english))


def getEncoding(data):
    """
    receives byes of data from opening HTML file,
    returns the appropriate codec i.e 'utf-8' or 'windows-1255'
    :param data:
    :return:
    """
    return re.findall(r"(?i)charset=\"?([^\s]+)\"", str(data))[0]


def getHtmlDataFromURL(url: str):
    f = urlopen(url)
    return f.read()


def getHTMLDataFromUG(courseId):
    return getHtmlDataFromURL(Addresses.TechnionUg + str(courseId))


def getHTMLDataFromGrad(courseId):
    return getHtmlDataFromURL(Addresses.TechnionGrad + str(courseId))


def parseDataFromGraduate(data, courseId):
    pass


def listSubFaculties():
    result = sorted(list(set([coursenum[:3] for coursenum in Courses])))
    print("subfaculties: ", result)
    return result


def listAllCourses():
    List = []
    for subfaculty in listSubFaculties():
        List.extend([subfaculty + str(num).zfill(3) for num in range(1000)])

        # if len(faculty) == 2:
        #     List.extend([faculty + digit + str(num).zfill(3) for num in range(1000) for digit in ThirdDigit])
        # elif len(faculty) == 3:
        #     List.extend([faculty + str(num).zfill(3) for num in range(1000)])
    # print(List[:100])
    return List


def courseOnUg(courseId):
    # print("trying course " + str(courseId))
    data = getHTMLDataFromUG(courseId)
    strData = str(data, encoding='utf8')
    # if not (len(re.findall("לא קיים", strData)) > 0):
    #     print("===ON UG===")
    # else:
    #     print("===NOT ON UG===")
    return not (len(re.findall("לא קיים", strData)) > 0)


def downloadCourse(courseId):
    try:
        # if (False == courseExists(courseId)):
        # data = getHTMLDataFromUG(courseId)

        # strData = str(data, encoding='utf8')
        # if (len(re.findall("לא קיים", strData)) > 0):
        # get and parse from graduate
        # return
        course = Courses[courseId]
        info = fetch_course(courseId)
        if not info:  # meaning the course isn't on UG, try on graduate
            info = parseGraduate(courseId)
        course.name = info.get('name', "")
        # course.kdams = info.get('מקצועות קדם', [])
        # course.zamuds = info.get('מקצועות צמודים', [])

        course.kdams = info.get('kdam', [])
        course.zamuds = info.get('adjacent', [])

        course.moed_A = info.get('exam_A', "")
        course.moed_B = info.get('exam_B', "")
        # else:
        #     course.name = info.get('name', "")
        #     course.kdams = info.get('kdam', [])
        #     course.zamuds = info.get('adjacent', [])
        #     if 'exam_A' in info:
        #         course.moed_A = ".".join(re.search("\d{1,2}\.\d{1,2}\.\d{4}", info['exam_A'])[0].split(".")[0:2])
        #     if 'exam_B' in info:
        #         course.moed_B = ".".join(re.search("\d{1,2}\.\d{1,2}\.\d{4}", info['exam_B'])[0].split(".")[0:2])

        toPickle(info, "data/pickle/info-" + courseId + ".p")
        # print(info)

        # Courses[courseId].name = getSubject(strData)
        # Courses[courseId].kdams = getKdams(strData)
        # Courses[courseId].zamuds = getZamuds(strData)
        # Courses[courseId].moed_A, Courses[courseId].moed_B = getExams(strData)

        # check if this course exists in UG:
        # if (len(re.findall("לא קיים", strData)) > 0):
        #     data = getHTMLDataFromGrad(courseId)
        #     parseDataFromGraduate(data, courseId)

        # open(htmlPath + "\\" + str(courseId) + ".htm", "wb").write(data)

        # sleep(1)
    except:
        pass
    # randomSleep()


def getKdams(data):
    try:
        kdams = list(set(re.findall(courseRegex, re.findall("מקצועות קדם.*?/div><div", data, re.DOTALL)[0])))
        kdams = list(set([CourseNum(x).id for x in kdams]))
    except:
        kdams = []
    return kdams


def extract_info(html):
    div_fmt = r'<div class="{}">\s*(.*?)\s*</div>'
    keys = re.findall(div_fmt.format('property'), html)
    values = re.findall(div_fmt.format('property-value'), html)
    # print("found " + str(values))
    return OrderedDict(zip(keys, [re.sub('\s+', ' ', v) for v in values]))


def fix(k, v):
    """
    kdam and adjacent are lists of lists, the rest are lists
    :param k:
    :param v:
    :return:
    """
    # TODO: fix exam dates so they're uniform with graduate parser
    data_title = r'data-original-title="(.*?)"'
    if k in ['kdam', 'adjacent']:
        return [re.findall(data_title, x) for x in v.split(' או ')]
    if k.startswith('no_more') or k in ['identical']:
        return re.findall(data_title, v)
    if k in ['site']:
        return re.search(r'href="(.*?)" ', v).group(1)
    if k in ['exam_A', 'exam_B']:
        return ".".join(re.search("\d{1,2}\.\d{1,2}\.\d{4}", v)[0].split(".")[0:2])
    return v


def cleanup(raw_dict):
    od = OrderedDict((trans[k], fix(trans[k], v))
                     for k, v in raw_dict.items())
    # if trans[k] not in irrelevant) ### I want test dates as well
    if not od:
        return {}
    if 'points' in od:
        od.move_to_end('points', last=False)
    od.move_to_end('id', last=False)
    if 'site' in od:
        od.move_to_end('site')
    od.move_to_end('syllabus')
    return od


def fetch(url):
    with request.urlopen(url) as w:
        return w.read().decode('utf8')


def read_course(number):
    return fetch("https://ug3.technion.ac.il/rishum/course/{}".format(number))


def fetch_course(number):
    return cleanup(extract_info(read_course(number)))


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


def getExams(data: str) -> List[str]:
    exams: List[str] = re.findall(">.*(\d\d\.\d\d).*" + Semester.TestYear.value, data)

    if (len(exams) > 1):
        return exams[:2]
    elif (len(exams) == 1):
        return [exams[0], ""]
    else:
        return ["", ""]


# def getCourseInfo(courseId):
#     path = htmlPath + "\\" + str(courseId) + ".htm"
#     try:
#         with open(path, mode='r', encoding='utf8') as file:
#             strData = file.read()
#             Courses[courseId].name = getSubject(strData)
#             Courses[courseId].kdams = getKdams(strData)
#             Courses[courseId].zamuds = getZamuds(strData)
#             Courses[courseId].moed_A, Courses[courseId].moed_B = getExams(strData)
#     except UnicodeDecodeError:
#         with open(path, mode='r', encoding='windows-1255') as file:
#             strData = file.read()
#             htmlParser = MyHTMLParser()
#             htmlParser.feed(strData)
#             Courses[courseId].name = htmlParser.name
#     finally:
#         os.remove(path)


def updateFollowups():
    for courseId, course in Courses.items():
        for kdamList in course.kdams:
            for kdam in kdamList:
                if kdam in Courses:
                    Courses[kdam].followups.append(courseId)
                else:
                    # print(kdam)
                    GraduateOnlyClasses.add(kdam)

    for courseId, course in Courses.items():
        course.followups = list(set(course.followups))


def updateReverseZamuds():
    for courseId, course in Courses.items():
        for zamudList in course.zamuds:
            for zamud in zamudList:
                if zamud in Courses:
                    Courses[zamud].reverseZamuds.append(courseId)
                else:
                    # print(zamud)
                    GraduateOnlyClasses.add(zamud)

    for courseId, course in Courses.items():
        course.reverseZamuds = list(set(course.reverseZamuds))


def updateCourses():
    for i, course in enumerate(Courses.keys()):
        print(str(i + 1), "/", len(Courses.keys()), " [{}]".format(course.id))
        downloadCourse(course)

    updateFollowups()
    updateReverseZamuds()


# for course in Courses:
#     getCourseInfo(course)

# # in case some files are not included in Courses:
# for x in os.listdir(htmlPath):
#     if os.path.isfile(os.path.join(htmlPath, x)):
#         courseId = CourseNum(os.path.splitext(x)[0])
#         Faculties[courseId.faculty()].courses.append(courseId)
#
#         Courses[courseId] = Course(courseId)
#         getCourseInfo(courseId)

# print(Courses[CourseNum("234123")].followups)
# print(Courses[CourseNum("234123")].kdams)
# print(Courses[CourseNum("234123")].zamuds)
# print(Courses[CourseNum("234123")].name)

def removeCourses(typoCourses):
    for courseId, course in Courses.items():
        for zamudList in course.zamuds:
            for zamud in zamudList:
                if zamud in typoCourses:
                    zamudList.remove(zamud)
                    if not zamudList:
                        course.zamuds.remove(zamudList)

    for courseId, course in Courses.items():
        for kdamList in course.kdams:
            for kdam in kdamList:
                if kdam in typoCourses:
                    kdamList.remove(kdam)
                    if not kdamList:
                        course.kdams.remove(kdamList)

    for facultyCode, faculty in Faculties.items():
        faculty.courses = [x for x in faculty.courses if x not in typoCourses]

    for course in typoCourses:
        Courses.pop(course, None)


if __name__ == "__main__":
    Faculties: Dict[str, Faculty] = fromPickle(Paths.picklePath.value + "\\faculties.p")
    Courses: Dict[CourseNum, Course] = fromPickle(Paths.picklePath.value + "\\courses.p")
    GraduateOnlyClasses: Set[CourseNum] = set()

    updateCourses()

    # updateFollowups()
    # updateReverseZamuds()

    print(
        "found {} courses listed as kdam/zamud listed only on Graduate, not included in database, writing to graduate_only_courses.txt".format(
            len(GraduateOnlyClasses)))
    with open("graduate_only_courses.txt", 'w') as file:
        printInLines(GraduateOnlyClasses, file=file)

    typoCourses = [k for k, v in Courses.items() if v.name == 'z/OS (CICS)']
    print("found {} courses with bad course numbers, writing to typo_courses.txt and removing from database".format(
        len(typoCourses)))
    with open("typo_courses.txt", 'w') as file:
        printInLines(typoCourses, file=file)

    removeCourses(typoCourses)

    # testCourses = ['234123','236335']
    # for x in testCourses:
    #     downloadCourse(x)

    # info = fetch_course('234123')
    # print(info)
    # moed_A = info.get('exam_A', "")
    # moed_A_split = moed_A.split('.')
    # moed_A_re = re.search("\d{1,2}\.\d{1,2}\.\d{4}", info['exam_A'])
    # # print(moed_A_re[0].split(".")[0:2])
    # print(".".join(moed_A_re[0].split(".")[0:2]))
    # print(moed_A_re[0])
    # print(moed_A)
    # print(moed_A_split)

    # info2 = fetch_course("238739")
    # print(info2)
    # print(listAllCourses())
    # megalist = listAllCourses()
    # print("length of megalist = " + str(len(megalist)))
    # filteredlist = filter(lambda x: courseOnUg(x) and CourseNum(x) not in Courses.keys(), megalist)
    # print(list(filteredlist))

    toPickle(Faculties, Paths.picklePath.value + r"\facultiesUpdated.p")
    toPickle(Courses, Paths.picklePath.value + r"\coursesUpdated.p")
