import os
from typing import Dict

from KdamClasses import Course, Faculty, CourseNum
from utils import fromPickle, Paths, toJSONFile, toPickle


class dataManager:
    faculties: Dict[str, Faculty]
    courses: Dict[CourseNum, Course]
    facFile = "faculties.p"
    courseFile = "courses.p"

    def __init__(self, fromFiles: bool = False):
        if fromFiles:
            self.faculties = self.getFaculties()
            self.courses = self.getCourses()
        else:
            self.faculties = {}
            self.courses = {}

    def getFaculties(self) -> Dict[str, Faculty]:
        return fromPickle(os.path.join(Paths.picklePath.value, self.facFile))

    def getCourses(self) -> Dict[CourseNum, Course]:
        return fromPickle(os.path.join(Paths.picklePath.value, self.courseFile))

    def writeToFiles(self) -> None:
        toJSONFile(self.faculties, os.path.join(Paths.jsonPath.value, self.facFile))
        toJSONFile(self.courses, os.path.join(Paths.jsonPath.value, self.courseFile))
        toPickle(self.faculties, os.path.join(Paths.picklePath.value, self.facFile))
        toPickle(self.courses, os.path.join(Paths.picklePath.value, self.courseFile))
