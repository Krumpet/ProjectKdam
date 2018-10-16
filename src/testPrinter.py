from typing import Set

from KdamClasses import *
from utils import *

Faculties: FacultiesDB = from_pickle(Paths.pickleNewFaculties)
Courses: CoursesDB = from_pickle(Paths.pickleNewCourses)
facultyTests = {}


def print_tests(faculty_to_print: str) -> None:
    course_nums: Set[CourseNum] = {x for x in Faculties[faculty_to_print].courses if
                                   x in Courses and (Courses[x].moed_A != "" or Courses[x].moed_B != "")}

    moed_as = {(Courses[num].moed_A, num, Courses[num].name) for num in course_nums if Courses[num].moed_A != ""}
    moed_bs = {(Courses[num].moed_B, num, Courses[num].name) for num in course_nums if Courses[num].moed_B != ""}
    sorted_as = sorted(moed_as, key=lambda tup: [int(x) for x in tup[0].split('.')[::-1]])
    sorted_bs = sorted(moed_bs, key=lambda tup: [int(x) for x in tup[0].split('.')[::-1]])

    with open(os.path.join(Paths.testPath, "{}-{}.txt".format(faculty_to_print, Faculties[faculty_to_print].name)),
              mode='w+') as file:
        print("Exam dates for faculty {} - {}\n".format(faculty_to_print, Faculties[faculty_to_print].name), file=file)
        print("Moed-A:", file=file)
        print("\n".join("{:7} {!s:7} {:>35}".format(tup[0], tup[1], tup[2]) for tup in sorted_as), file=file)
        print("Moed-B:", file=file)
        print("\n".join("{:7} {!s:7} {:>35}".format(tup[0], tup[1], tup[2]) for tup in sorted_bs), file=file)

    sorted_as.extend(sorted_bs)
    if sorted_as:
        facultyTests[faculty_to_print] = sorted_as
    # sorted_Tests = sorted_as[:]
    # sorted_Tests.extend(sorted_bs)
    # toJSONFile(sorted_Tests, "data/json/{}-tests.json".format(faculty))

    # print(Moed_As)

    # print(list(setToSort).sort(key=lambda tup: [str(x) for x in tup[2].split('.')]))

    # print(setToSort)

# TODO: wrap this up in a test printer
for faculty in Faculties:
    # for faculty in ['23']:
    #     print(faculty)
    print_tests(faculty)
    # print("========")

    # files are not modified, so only save tests
    to_json_file(facultyTests, Paths.jsonTests)  # , indent=0)
    # toJSONFile(dictRecursiveFormat(Courses), Paths.jsonNewCourses)
    # toJSONFile(Faculties, os.path.join(Paths.jsonPath ,"facultiesUpdated.json"))

# toPickle(Faculties, picklePath + r"\facultiesUpdated.p")
# TODO: put in "main" function

"""
Note for the future: Currently run "pdfToDataParser" and then "downloadUpdateCourses" and then "testPrinter"
"""
