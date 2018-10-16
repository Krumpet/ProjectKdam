from KdamClasses import FacultiesDB, CoursesDB
from utils import from_pickle


class DataManager:
    faculties: FacultiesDB
    courses: CoursesDB

    def __init__(self, from_files: bool = False, faculty_file_path: str = None, course_file_path: str = None) -> None:
        if from_files:
            self.faculties = self.get_faculties(faculty_file_path)
            self.courses = self.get_courses(course_file_path)
        else:
            self.faculties = {}
            self.courses = {}

    @staticmethod
    def get_faculties(faculties_file_path) -> FacultiesDB:
        return from_pickle(faculties_file_path)

    @staticmethod
    def get_courses(courses_file_path) -> CoursesDB:
        return from_pickle(courses_file_path)
    #
    # def writeToFiles(self) -> None:
    #     toJSONFile(self.faculties, os.path.join(Paths.jsonPath.value, self.facFile))
    #     toJSONFile(self.courses, os.path.join(Paths.jsonPath.value, self.courseFile))
    #     toPickle(self.faculties, os.path.join(Paths.picklePath.value, self.facFile))
    #     toPickle(self.courses, os.path.join(Paths.picklePath.value, self.courseFile))

    def purge(self):
        self.faculties.clear()
        self.courses.clear()
