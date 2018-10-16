import re
from typing import List

from KdamClasses import Course, CourseNum, Faculty
from DataManager import DataManager
from utils import *


class TxtParser:
    # manager: dataManager

    # def __init__(self, manager: dataManager = dataManager()):
    #     manager = manager

    @staticmethod
    def parse_texts(manager: DataManager, target_dir: str):
        # numOfPages = getPdfPageNum(fileName=fileName)

        # def txtFilename(index: int):
        #     # TODO: refactor so basefilename is saved once in txt/pdf manager
        #     baseTxtFilename = fileName.replace(".pdf", "")

        # manager = dataManager()
        # faculties = manager.faculties
        # TODO: replace page number iteration with iterating over text files
        # specify the format of text files - should contain faculty code and name like in pdf catalogue,
        # or make that part optional
        # for i in range(1, numOfPages + 1):
        for file in os.scandir(target_dir):
            if not file.is_file():
                continue
            # tempOpen closes and deletes the text file after use
            # with tempOpen(txtPath + "\\" + FileName + str(i) + Suffix, 'r', encoding="utf8") as file:
            # TODO: use temp_open
            with open(file.path, "r", encoding="utf8") as f:
                # with open(Paths.txtPath.value + "\\" + FilenameConsts.FileName.value + str(i) +
                # FilenameConsts.Suffix.value, 'r', encoding="utf8") as file:
                data: List[str] = []
                try:
                    data = [" ".join(line.split()).strip() for line in f.readlines()]
                    # if not data or ... and take out of 'with' scope
                    # if text is not flipped, use data[0][::-1] to flip the line
                    if re.search("תו?כנית לימודים", data[0], re.DOTALL) is None:
                        continue
                    """
                    The title of pages that contain class lists for each faculty have the format:
                    2017/2018 Blah blah blah / 23 Computer Science
                    So we capture the '23' and the 'Computer Science'
                    """
                    # print('got here for real page')
                    # print(data[0])
                    # Use this then text is reversed in the text files:
                    # faculty_code, faculty_name = re.findall("\d+.\d+ +.* +/ +(\d+) +(.*)", data[0])[0]
                    # Use this if you bothered to flip the Hebrew text in the text files
                    faculty_name, faculty_code = re.findall("(.*) +(\d{2,3}) +/ +.* \d+[/-]\d+", data[0])[0]

                    # Some faculties don't have a faculty code, producing a "list index out of range" error when trying
                    # to find the faculty name and code. e.g.:
                    # "list index out of range אנרגיה / תוכנית לימודים תשע"ח 2017/2018"

                    # print('used regex on real page')

                    # if text is not flipped, faculty name is captured in reverse so flip it
                    # faculty_name = faculty_name[::-1]

                    # TODO: maybe combine data from lines to one big string?
                    # course_in_each_line = [re.findall(courseRegex, data[j]) for j in range(len(data))]
                    # courses_on_this_page = list(
                    #     set([CourseNum(courseNum) for sublist in course_in_each_line for courseNum in sublist]))
                    # TODO: TESTING joining all lines and then doing regex search

                    # TODO: move all addition logic to the data manager
                    course_in_each_line = re.findall(course_regex, "\n".join(data))
                    # TODO: split courses into self_courses and other_courses
                    courses_on_this_page = list(
                        set([CourseNum(courseNum) for courseNum in course_in_each_line]))

                    course_objects = [manager.courses.get(courseId, Course(courseId)) for courseId in
                                      courses_on_this_page]
                    for course in course_objects:
                        if course.courseId not in manager.courses:
                            manager.courses[course.courseId] = course
                        faculty = course.faculty()
                        # todo: this is possibly avoided by using a defaultkeydict - trying to access the faculty will
                        # create a default one with no name
                        if faculty not in manager.faculties:
                            manager.faculties[faculty] = Faculty(faculty)
                        if course.courseId not in manager.faculties[faculty].courses:
                            manager.faculties[faculty].courses.append(course.courseId)
                    if faculty_code not in manager.faculties:
                        manager.faculties[faculty_code] = Faculty(faculty_code, faculty_name)
                    # else:
                    #     if Faculties[faculty_code].name == "":
                    #         Faculties[faculty_code].name = faculty_name
                    manager.faculties[faculty_code].add_courses(courses_on_this_page)
                    if manager.faculties[faculty_code].name == "":
                        # if created earlier without a name, make sure to update it
                        manager.faculties[faculty_code].name = faculty_name

                    print("reading faculty {0}, faculty code {1}".format(faculty_name, faculty_code))
                except Exception as e:
                    print(e, data[0] if len(data) > 0 else "no text found on page")
                    continue

    @staticmethod
    def update_extra_courses(manager: DataManager) -> None:
        # TODO: save this path externally
        with open('../ug-fetch/metadata/course_ids.txt') as file:
            raw_courses = file.readlines()
        courses = [CourseNum(x.strip()) for x in raw_courses]
        course_nums = [x for x in courses if x not in manager.courses]
        print("adding {} classes".format(len(course_nums)))
        for course_num in course_nums:
            manager.courses[course_num] = Course(course_num)
            faculty = course_num.faculty()
            if faculty not in manager.faculties:
                print("adding faculty {}".format(faculty))
                manager.faculties[faculty] = Faculty(faculty, "")
            print("adding course {} to faculty {}".format(course_num, faculty))
            manager.faculties[faculty].courses.append(course_num)

    @staticmethod
    def update_extra_courses_from_txt(manager: DataManager) -> None:
        """
        Get courses from extra files in the "txtPath" directory, and
        add them to the main Courses list, and the appropriate Faculty
        :return:
        """
        for x in os.listdir(Paths.txtPath):
            path = os.path.join(Paths.txtPath, x)
            if os.path.isfile(path):
                print("got file ", path)
                with temp_open(path, 'r') as file:
                    data = file.read()
                courses_numbers = list(set(re.findall(course_regex, data, re.DOTALL)))
                course_num_list = [CourseNum(x) for x in courses_numbers]
                for course_number in course_num_list:
                    if course_number not in manager.courses:
                        manager.courses[course_number] = Course(course_number)
                        if course_number.faculty() not in manager.faculties:
                            raise AttributeError(
                                "Faculty with code " + course_number.faculty() +
                                " not found in Faculties in catalogue!")
                        manager.faculties[course_number.faculty()].courses.append(course_number)

    #

    #
    # # def writeToFiles():
    # #     toJSONFile(Faculties, Paths.jsonPath + "\\faculties.json")
    # #     toJSONFile(Courses, Paths.jsonPath + "\\courses.json")
    # #     toPickle(Faculties, Paths.picklePath + "\\faculties.p")
    # #     toPickle(Courses, Paths.picklePath + "\\courses.p")
    #
    @staticmethod
    def typo_fixes(manager: DataManager) -> None:
        manager.courses.pop(manager.faculties['29'].courses[0], None)
        manager.courses.pop(manager.faculties['00'].courses[0], None)
        bad_courses = {CourseNum(x) for x in {'294901', '03042'}}
        manager.faculties['21'].courses = [x for x in manager.faculties['21'].courses if x not in bad_courses]
        manager.faculties.pop('29', None)
        manager.faculties.pop('00', None)
        manager.faculties['39'].name = 'קורסי ספורט'
    #
    # def writeToFiles(self):
    #     manager.writeToFiles()


if __name__ == "__main__":
    parser = TxtParser()

    # parser.parseTexts()
    # parser.updateExtraCourses()
    # # parser.typoFixes()  # some errors in the catalogue, I remove them manually
    # parser.pruneFaculties()
    # parser.writeToFiles()

# print(sorted(Courses.keys()))
# print(Faculties.keys())

# for k, v in Faculties.items():
#     print(k, v.courses)

# for k, v in Courses.items():
#     print(k)

# print(len(Courses.keys()))
#
# print(len(list(set(Courses.keys()))))
#
# totalcourse = []
#
# for k, v in Faculties.items():
#     totalcourse.extend(v.courses)
#
# totalcourse = list(set(totalcourse))
# print(len(totalcourse))

# print(Faculties["23"].courses)
#
# print(json.dumps(Courses, default=lambda x: x.__dict__))
#
# data = open(FilePath+"\\"+FileName, "r", encoding="utf8").read()
# data = open(r"C:\Users\ADMIN\PycharmProjects\Project_Kdam\data1\AllFacs.txt", "r").read()
# # print(data)
# pattern = r"חלק ' ד.*חלק ה"
# pattern2 = "TAG_START.*TAG_END"
# segment = re.findall(pattern2, data, re.DOTALL)
# print('\n'.join(segment))
# print(segment.string)
# print(len(segment))
# segment0 = segment[0]
#
# print(segment)
