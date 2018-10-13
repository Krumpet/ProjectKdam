import os
from typing import Dict, Type

from KdamClasses import Course, Faculty, CourseNum
from utils import fromPickle, Paths, toJSONFile, toPickle

CoursesDB: Type = Dict[CourseNum, Course]
FacultiesDB: Type = Dict[str, Faculty]

class dataManager:
    faculties: FacultiesDB
    courses: CoursesDB

    def __init__(self, fromFiles: bool = False, facultyFilePath: str = None, courseFilePath: str = None):
        if fromFiles:
            self.faculties = self.getFaculties(facultyFilePath)
            self.courses = self.getCourses(courseFilePath)
        else:
            self.faculties = {}
            self.courses = {}

    def getFaculties(self, fac) -> FacultiesDB:
        return fromPickle(fac)

    def getCourses(self, course) -> CoursesDB:
        return fromPickle(course)
    #
    # def writeToFiles(self) -> None:
    #     toJSONFile(self.faculties, os.path.join(Paths.jsonPath.value, self.facFile))
    #     toJSONFile(self.courses, os.path.join(Paths.jsonPath.value, self.courseFile))
    #     toPickle(self.faculties, os.path.join(Paths.picklePath.value, self.facFile))
    #     toPickle(self.courses, os.path.join(Paths.picklePath.value, self.courseFile))

    def purge(self):
        self.faculties.clear()
        self.courses.clear()
