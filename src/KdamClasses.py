from typing import List

# TODO: changer all lists to sets

class CourseNum():
    id: str

    def __init__(self, num):
        if (len(num) < 5):
            raise AttributeError("Course number too short at " + num)
        # super(CourseNum, self).__init__()
        self.id = num.zfill(6)
        # while (len(self.id) < 6):
        #     self.id = "0" + self.id

    # def __eq__(self, other):
    #     if isinstance(other, CourseNum):
    #         return self.id == other.id
    #     return NotImplemented

    def __str__(self):
        return self.id

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, CourseNum) and self.id == other.id

    def __ne__(self, other):
        return not (self == other)

    def __len__(self):
        return len(self.id)

    def faculty(self):
        """
        Tells us the faculty code of the course - currently 2 digits except for '500' type faculties
        """
        if self.id.startswith("5"):
            return self.id[:3]
        else:
            return self.id[:2]


class Course:
    courseId: CourseNum
    name: str
    moed_A: str
    moed_B: str
    kdams: List[List[CourseNum]]
    zamuds: List[List[CourseNum]]
    followups: List[CourseNum]
    reverseZamuds: List[CourseNum]

    def __init__(self, id, name="", Moed_A="", Moed_B="", Kdams=None, Zamuds=None, Followups=None, RZ=None):
        self.courseId = CourseNum(id)
        self.name = name
        self.moed_A = Moed_A
        self.moed_B = Moed_B
        self.kdams = Kdams if Kdams is not None else []
        self.zamuds = Zamuds if Zamuds is not None else []
        self.followups = Followups if Followups is not None else []
        self.reverseZamuds = RZ if RZ is not None else []

    def faculty(self):
        """
        Tells us the faculty code of the course - currently 2 digits except for '500' type faculties
        """
        return self.courseId.faculty()

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

    def __init__(self, id, name=""):
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

    def __str__(self):
        return self.__repr__()  # "Faculty: {} name: {}, has {} classes, subclasses are: {}".format(self.code, self.name,
        #                                                  len(self.courses),
        #                                                 sorted(set(
        #                                                    x[:3] for x in self.courses if
        #                                                   x.faculty() == self.code)))

    def __repr__(self):
        return "Faculty: {} name: {} classes: {} fac-classes: {} subfaculties are: {}".format(self.code, self.name,
                                                                                              len(self.courses),
                                                                                              len(set(x for x in
                                                                                                      self.courses if
                                                                                                      x.faculty() == self.code)),
                                                                                              sorted(set(
                                                                                                  x[:3] for x in
                                                                                                  self.courses if
                                                                                                  x.faculty() == self.code)))
