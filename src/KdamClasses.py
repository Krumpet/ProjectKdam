from typing import List, Type, Dict


# TODO: changer all lists to sets

class CourseNum:
    _id: str

    def __init__(self, num) -> None:
        # if len(num) < 5:
        #     raise AttributeError("Course number too short at " + num)
        # super(CourseNum, self).__init__()
        self.cid = str(num)  # .zfill(6)
        # while (len(self.id) < 6):
        #     self.id = "0" + self.id

    @property
    def cid(self):
        return self._id

    @cid.setter
    def cid(self, id):
        self._id = str(id).zfill(6)

    def __str__(self):
        return self.cid

    def __repr__(self):
        return 'cid: {}'.format(self.cid)

    def __hash__(self):
        return hash(self.cid)

    def __eq__(self, other):
        return isinstance(other, CourseNum) and self.cid == other.cid

    def __ne__(self, other):
        return not (self == other)

    def __len__(self):
        return len(self.cid)

    # For <, __lt__ is used.For >, __gt__.For <= and >=, __le__ and __ge__ respectively.
    def __lt__(self, other):
        if isinstance(other, CourseNum):
            return self.cid < other.cid
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, CourseNum):
            return self.cid > other.cid
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, CourseNum):
            return self.cid <= other.cid
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, CourseNum):
            return self.cid >= other.cid
        return NotImplemented

    def faculty(self):
        """
        Tells us the faculty code of the course - currently 2 digits except for '500' type faculties
        """
        return self.cid[:3] if self.cid.startswith("5") else self.cid[:2]
        # if self.cid.startswith("5"):
        #     return self.cid[:3]
        # else:
        #     return self.cid[:2]


class Course:
    courseId: CourseNum
    name: str
    moed_A: str
    moed_B: str
    kdams: List[List[CourseNum]]
    zamuds: List[List[CourseNum]]
    followups: List[CourseNum]
    reverseZamuds: List[CourseNum]

    def __init__(self, cid, name="", moed_a="", moed_b="", kdams=None, zamuds=None, followups=None,
                 reverse_zamuds=None) -> None:
        self.courseId = CourseNum(cid)
        self.name = name
        self.moed_A = moed_a
        self.moed_B = moed_b
        self.kdams = kdams if kdams is not None else []
        self.zamuds = zamuds if zamuds is not None else []
        self.followups = followups if followups is not None else []
        self.reverseZamuds = reverse_zamuds if reverse_zamuds is not None else []

    def faculty(self):
        """
        Tells us the faculty code of the course - currently 2 digits except for '500' type faculties
        """
        return self.courseId.faculty()

    # TODO: check if all of these operators are even in use
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

    def __init__(self, faculty_code, name="") -> None:
        self.code = faculty_code
        self.name = name
        # self.courses = {course : Course(course) for course in courseIds} if courseIds is not None else {}
        self.courses = []

    def add_courses(self, course_list: List[CourseNum]):
        if not course_list:
            return

        # if isinstance(courseList[0], str):
        #     for courseId in courseList:
        #         if courseId not in self.courses.keys():
        #             self.courses[courseId] = Course(courseId)

        # elif isinstance(courseList[0], Course):
        # self.courses.extend(courseList)
        # self.courses = list(set(self.courses))
        for course in course_list:
            if course not in self.courses:
                self.courses.append(course)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Faculty: {} name: {} classes: {} fac-classes: {} subfaculties are: {}" \
            .format(self.code, self.name,
                    len(self.courses),
                    len(set(x for x in
                            self.courses if
                            x.faculty() == self.code)),
                    sorted(set(
                        x[:3] for x in
                        self.courses if
                        x.faculty() == self.code)))


FacultiesDB: Type = Dict[str, Faculty]
CoursesDB: Type = Dict[CourseNum, Course]
