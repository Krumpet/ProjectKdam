from KdamClasses import FacultiesDB, CoursesDB
from utils import fromPickle


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
