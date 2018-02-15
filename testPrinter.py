from utils import *
from typing import Dict, Set
from KdamClasses import *

Faculties: Dict[str, Faculty] = fromPickle(picklePath + "\\facultiesUpdated.txt")
Courses: Dict[CourseNum, Course] = fromPickle(picklePath + "\\coursesUpdated.txt")


def printTests(faculty):
    courseNums = {x for x in Faculties[faculty].courses if
                  x in Courses and (Courses[x].moed_A != "" or Courses[x].moed_B != "")}

    Moed_As = {(num, Courses[num].name, Courses[num].moed_A) for num in courseNums if Courses[num].moed_A != ""}
    Moed_Bs = {(num, Courses[num].name, Courses[num].moed_B) for num in courseNums if Courses[num].moed_B != ""}
    sorted_As = sorted(Moed_As, key=lambda tup: [int(x) for x in tup[2].split('.')[::-1]])
    sorted_Bs = sorted(Moed_Bs, key=lambda tup: [int(x) for x in tup[2].split('.')[::-1]])
    # print(Moed_As)
    with open("data/tests/{}-{}.txt".format(faculty, Faculties[faculty].name), mode='w') as file:
        print("Exam dates for faculty {} - {}\n".format(faculty, Faculties[faculty].name), file=file)
        print("Moed-A:", file=file)
        print("\n".join("{:7} {:7} {:>35}".format(tup[2], tup[0], tup[1]) for tup in sorted_As), file=file)
        print("Moed-B:", file=file)
        print("\n".join("{:7} {:7} {:>35}".format(tup[2], tup[0], tup[1]) for tup in sorted_Bs), file=file)

    sorted_Tests = sorted_As[:]
    sorted_Tests.extend(sorted_Bs)
    toJSONFile(sorted_Tests, "data/json/{}-tests.json".format(faculty))

    # print(Moed_As)

    # print(list(setToSort).sort(key=lambda tup: [str(x) for x in tup[2].split('.')]))

    # print(setToSort)


for faculty in Faculties:
    # for faculty in ['23']:
    #     print(faculty)
    printTests(faculty)
    # print("========")

# toPickle(Faculties, picklePath + r"\facultiesUpdated.txt")
