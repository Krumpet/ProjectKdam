from typing import Dict, Set

from KdamClasses import *
from utils import *

Faculties: FacultiesDB = fromPickle(Paths.pickleNewFaculties)
Courses: CoursesDB = fromPickle(Paths.pickleNewCourses)
facultyTests = {}


def printTests(faculty: str) -> None:
    courseNums: Set[CourseNum] = {x for x in Faculties[faculty].courses if
                                  x in Courses and (Courses[x].moed_A != "" or Courses[x].moed_B != "")}

    Moed_As = {(Courses[num].moed_A, num, Courses[num].name) for num in courseNums if Courses[num].moed_A != ""}
    Moed_Bs = {(Courses[num].moed_B, num, Courses[num].name) for num in courseNums if Courses[num].moed_B != ""}
    sorted_As = sorted(Moed_As, key=lambda tup: [int(x) for x in tup[0].split('.')[::-1]])
    sorted_Bs = sorted(Moed_Bs, key=lambda tup: [int(x) for x in tup[0].split('.')[::-1]])
    # print(Moed_As)
    # TODO: use absolute paths here
    with open(os.path.join(Paths.testPath, "{}-{}.txt".format(faculty, Faculties[faculty].name)),
              mode='w+') as file:
        print("Exam dates for faculty {} - {}\n".format(faculty, Faculties[faculty].name), file=file)
        print("Moed-A:", file=file)
        print("\n".join("{:7} {!s:7} {:>35}".format(tup[0], tup[1], tup[2]) for tup in sorted_As), file=file)
        print("Moed-B:", file=file)
        print("\n".join("{:7} {!s:7} {:>35}".format(tup[0], tup[1], tup[2]) for tup in sorted_Bs), file=file)

    sorted_As.extend(sorted_Bs)
    if sorted_As:
        facultyTests[faculty] = sorted_As
    # sorted_Tests = sorted_As[:]
    # sorted_Tests.extend(sorted_Bs)
    # toJSONFile(sorted_Tests, "data/json/{}-tests.json".format(faculty))

    # print(Moed_As)

    # print(list(setToSort).sort(key=lambda tup: [str(x) for x in tup[2].split('.')]))

    # print(setToSort)


for faculty in Faculties:
    # for faculty in ['23']:
    #     print(faculty)
    printTests(faculty)
    # print("========")

    # files are not modified, so only save tests
    toJSONFile(facultyTests, Paths.jsonTests)  # , indent=0)
    # toJSONFile(dictRecursiveFormat(Courses), Paths.jsonNewCourses)
    # toJSONFile(Faculties, os.path.join(Paths.jsonPath ,"facultiesUpdated.json"))

# toPickle(Faculties, picklePath + r"\facultiesUpdated.p")
# TODO: put in "main" function

"""
Note for the future: Currently run "pdfToDataParser" and then "downloadUpdatCourses" and then "testPrinter"
"""
