import os
from typing import Set, Tuple, List, Dict

from KdamClasses import FacultiesDB, CoursesDB, CourseNum
from Utils import from_pickle, to_json_file
from Consts import Paths


class TestPrinter:
    faculties: FacultiesDB
    courses: CoursesDB
    # TODO: make these tuples into a type of their own (namedtuples?)
    faculties_tests: Dict[str, List[Tuple[str, CourseNum, str]]] = {}

    def __init__(self, courses: CoursesDB = None, faculties: FacultiesDB = None) -> None:
        self.courses = from_pickle(Paths.PICKLE_COURSES) if courses is None else courses
        self.faculties = from_pickle(Paths.PICKLE_FACULTIES) if faculties is None else faculties
        self.faculties_tests = {}

    def print_tests_for_faculty(self, fac_code: str) -> None:
        course_nums: Set[CourseNum] = {x for x in self.faculties[fac_code].courses if
                                       x in self.courses and (
                                               self.courses[x].moed_a != "" or self.courses[x].moed_b != "")}

        moed_as: Set[Tuple[str, CourseNum, str]] = {(self.courses[num].moed_a, num, self.courses[num].name) for num in
                                                    course_nums
                                                    if
                                                    self.courses[num].moed_a != ""}
        moed_bs: Set[Tuple[str, CourseNum, str]] = {(self.courses[num].moed_b, num, self.courses[num].name) for num in
                                                    course_nums
                                                    if
                                                    self.courses[num].moed_b != ""}
        sorted_as = sorted(moed_as, key=lambda tup: [int(x) for x in tup[0].split('.')[::-1]])
        sorted_bs = sorted(moed_bs, key=lambda tup: [int(x) for x in tup[0].split('.')[::-1]])

        with open(os.path.join(Paths.TEST_PATH,
                               "{}-{}.txt".format(fac_code, self.faculties[fac_code].name)),
                  mode='w+') as file:
            print("Exam dates for faculty {} - {}\n".format(fac_code, self.faculties[fac_code].name),
                  file=file)
            print("Moed-A:", file=file)
            print("\n".join("{:7} {!s:7} {:>35}".format(tup[0], tup[1], tup[2]) for tup in sorted_as), file=file)
            print("Moed-B:", file=file)
            print("\n".join("{:7} {!s:7} {:>35}".format(tup[0], tup[1], tup[2]) for tup in sorted_bs), file=file)

        sorted_as.extend(sorted_bs)
        if sorted_as:
            self.faculties_tests[fac_code] = sorted_as

    def print_tests(self):
        # populate test list for each faculty
        print("building test lists for each faculty and writing them to files",
              "output will be at" + Paths.TEST_PATH)
        for faculty_code in self.faculties:
            # TODO: change to just populating lists, print in separate function
            self.print_tests_for_faculty(faculty_code)
        to_json_file(self.faculties_tests, Paths.JSON_TESTS)


def main():
    printer = TestPrinter()
    printer.print_tests()


if __name__ == "__main__":
    # Note for the future: Currently run "pdfToDataParser" and then "downloadUpdateself.courses" and then "testPrinter"
    main()
