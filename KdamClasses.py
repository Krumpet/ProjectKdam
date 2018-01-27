# import Course
# from Course import Course
from typing import Dict, List, Union
from utils import htmlPath
from html.parser import HTMLParser


class CourseNum(str):
    id: str

    def __init__(self, str=""):
        if (len(str) < 5):
            raise AttributeError("Course number too short at " + str)
        super(CourseNum, self).__init__()
        self.id = str
        while (len(self.id) < 6):
            self.id = "0" + self.id
        # if (len(self.id) < 6):
        #     self.id = "0" + self.id

    def __str__(self):
        return self.id


class Course:
    courseId: CourseNum
    name: str
    moed_A: str
    moed_B: str
    kdams: List[CourseNum]  # list
    zamuds: List[CourseNum]  # list
    followups: List[CourseNum]  # list

    def __init__(self, id, name="", Moed_A="None", Moed_B="None", Kdams=None, Zamuds=None, Followups=None):
        self.courseId = CourseNum(id)
        self.name = name
        self.moed_A = Moed_A
        self.moed_B = Moed_B
        self.kdams = Kdams if Kdams is not None else []
        self.zamuds = Zamuds if Zamuds is not None else []
        self.followups = Followups if Followups is not None else []

    def faculty(self):
        """
        Tells us the faculty code of the course - currently 2 digits except for '500' type faculties
        """
        if self.courseId.startswith("5"):
            return self.courseId[:3]
        else:
            return self.courseId[:2]

    def __eq__(self, other):
        if isinstance(other, Course):
            return self.courseId == other.courseId
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    # For <, __lt__ is used.For >, __gt__.For <= and >=, __le__ and __ge__ respectively.
    def __lt__(self, other):
        if isinstance(other, Course):
            return self.courseId < other.courseId
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Course):
            return self.courseId > other.courseId
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Course):
            return self.courseId <= other.courseId
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Course):
            return self.courseId >= other.courseId
        return NotImplemented

    def __str__(self):
        return "Course {0} ID: {1}, Kdams: {2}, " \
               "followups: {3}, Moed A: {4}, Moed B: {5}".format(self.name,
                                                                 self.courseId,
                                                                 self.kdams,
                                                                 self.followups,
                                                                 self.moed_A,
                                                                 self.moed_B)


class Faculty:
    code: str
    name: str
    # courses: Dict[str, Course]
    courses: List[CourseNum]

    def __init__(self, id: str, name: str):
        self.code = id
        self.name = name
        # self.courses = {course : Course(course) for course in courseIds} if courseIds is not None else {}
        self.courses = []

    def addCourses(self, courseList: List[CourseNum]):
        if courseList == []:
            return

        # if isinstance(courseList[0], str):
        #     for courseId in courseList:
        #         if courseId not in self.courses.keys():
        #             self.courses[courseId] = Course(courseId)

        # elif isinstance(courseList[0], Course):
        # self.courses.extend(courseList)
        # self.courses = list(set(self.courses))
        for course in courseList:
            if course not in self.courses:
                self.courses.append(course)


class MyHTMLParser(HTMLParser):
    # Initialize lists
    name = ""
    kdams = []
    zamuds = []
    latestStartTag = ""
    gotTitle: bool = True

    def handle_starttag(self, startTag, attrs):
        self.latestStartTag = startTag
        self.gotTitle = False

    def handle_data(self, data: str):
        if self.latestStartTag == "title" and not self.gotTitle:
            self.gotTitle = True
            self.name = data.split(":")[1].split("-")[0].strip()
