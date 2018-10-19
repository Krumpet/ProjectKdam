from typing import List, Type, Dict, Collection


# TODO: change all lists to sets (of lists or frozensets)

class CourseNum:
    _id: str

    def __init__(self, num) -> None:
        if len(num) < 5:
            raise AttributeError("Course number too short at " + num)
        self.cid = str(num)

    @property
    def cid(self):
        return self._id

    @cid.setter
    def cid(self, c_id):
        self._id = str(c_id).zfill(6)

    def __str__(self):
        return self.cid

    def __repr__(self):
        return 'cid: {}'.format(self.cid)

    def __hash__(self):
        return hash(self.cid)

    def __eq__(self, other):
        return isinstance(other, CourseNum) and self.cid == other.cid

    def __ne__(self, other):
        return not self == other

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
        return self.cid[:2] if not self.cid.startswith("5") else self.cid[:3]


class Course:
    course_id: CourseNum
    name: str
    moed_a: str
    moed_b: str
    kdams: List[List[CourseNum]]
    zamuds: List[List[CourseNum]]
    followups: List[CourseNum]
    reverse_zamuds: List[CourseNum]

    # def __init__(self, cid, name="", moed_a="", moed_b="", kdams=None, zamuds=None, followups=None,
    #              reverse_zamuds=None) -> None:
    # TODO: testing creation with only code, as other data is obtained later
    def __init__(self, cid) -> None:
        self.course_id = CourseNum(cid)
        self.name = ""
        self.moed_a = ""
        self.moed_b = ""
        self.kdams = []
        self.zamuds = []
        self.followups = []
        self.reverse_zamuds = []

    def faculty(self):
        """
        Tells us the faculty code of the course - currently 2 digits except for '500' type faculties
        """
        return self.course_id.faculty()

    # TODO: check if all of these operators are even in use
    def __eq__(self, other):
        if isinstance(other, Course):
            return self.course_id == other.course_id
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    # For <, __lt__ is used.For >, __gt__.For <= and >=, __le__ and __ge__ respectively.
    def __lt__(self, other):
        if isinstance(other, Course):
            return self.course_id < other.course_id
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Course):
            return self.course_id > other.course_id
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Course):
            return self.course_id <= other.course_id
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Course):
            return self.course_id >= other.course_id
        return NotImplemented

    def __str__(self):
        return "Course {0} ID: {1}, Kdams: {2}, " \
               "followups: {3}, Moed A: {4}, Moed B: {5}".format(self.name,
                                                                 self.course_id,
                                                                 self.kdams,
                                                                 self.followups,
                                                                 self.moed_a,
                                                                 self.moed_b)

    def __hash__(self):
        return hash(self.course_id)


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

    def add_courses(self, course_list: Collection[CourseNum]):
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

    def __hash__(self):
        return hash(self.code)


FacultiesDB: Type = Dict[str, Faculty]
CoursesDB: Type = Dict[CourseNum, Course]
