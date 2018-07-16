from KdamClasses import Course, CourseNum
from dataManager import dataManager
from pdfParser import getPdfPageNum
from utils import *


# TODO: split creation of these objects to another file and load them here


# faculties: Dict[str, Faculty] = {}
# courses: Dict[CourseNum, Course] = {}

class txtParser:
    manager: dataManager

    def __init__(self, manager: dataManager = dataManager(fromFiles=False)):
        self.manager = manager

    def parseTexts(self):
        numOfPages = getPdfPageNum()
        # manager = dataManager()
        # faculties = manager.faculties
        # TODO: replace page number iteration with iterating over text files
        # specify the format of text files - should contain faculty code and name like in pdf catalogue,
        # or make that part optional
        for i in range(1, numOfPages + 1):
            # tempOpen closes and deletes the text file after use
            # with tempOpen(txtPath + "\\" + FileName + str(i) + Suffix, 'r', encoding="utf8") as file:
            with open(Paths.txtPath + "\\" + FilenameConsts.FileName + str(i) + FilenameConsts.Suffix, 'r',
                      encoding="utf8") as file:
                try:
                    data = [" ".join(line.split()).strip() for line in file.readlines()]
                    # if not data or ... and take out of 'with' scope
                    # if text is not flipped, use data[0][::-1] to flip the line
                    if re.search("תו?כנית לימודים", data[0], re.DOTALL) is None:
                        continue
                    """
                    The title of pages that contain class lists for each faculty have the format:
                    2017/2018 Blah blah blah / 23 Computer Science
                    So we capture the '23' and the 'Computer Science'
                    """
                    facultyCode, facultyName = re.findall("\d+.\d+ +.* +/ +(\d+) +(.*)", data[0])[0]

                    # if text is not flipped, faculty name is captured in reverse so flip it
                    # facultyName = facultyName[::-1]

                    # TODO: maybe combine data from lines to one big string?
                    # courseInEachLine = [re.findall(courseRegex, data[j]) for j in range(len(data))]
                    # coursesOnThisPage = list(
                    #     set([CourseNum(courseNum) for sublist in courseInEachLine for courseNum in sublist]))
                    # TODO: TESTING joining all lines and then doing regex search

                    # TODO: move all addition logic to the data manager
                    courseInEachLine = re.findall(courseRegex, "\n".join(data))
                    coursesOnThisPage = list(
                        set([CourseNum(courseNum) for courseNum in courseInEachLine]))

                    courseObjects = [self.manager.courses.get(courseId, Course(courseId)) for courseId in
                                     coursesOnThisPage]
                    for course in courseObjects:
                        if course.courseId not in self.manager.courses:
                            self.manager.courses[course.courseId] = course
                        faculty = course.faculty()
                        if faculty not in self.manager.faculties:
                            self.manager.faculties[faculty] = Faculty(faculty, "")
                        if course.courseId not in self.manager.faculties[faculty].courses:
                            self.manager.faculties[faculty].courses.append(course.courseId)
                    if facultyCode not in self.manager.faculties:
                        self.manager.faculties[facultyCode] = Faculty(facultyCode, facultyName)
                    # else:
                    #     if Faculties[facultyCode].name == "":
                    #         Faculties[facultyCode].name = facultyName
                    self.manager.faculties[facultyCode].addCourses(coursesOnThisPage)
                    if self.manager.faculties[
                        facultyCode].name == "":  # if created earlier without a name, make sure to update it
                        self.manager.faculties[facultyCode].name = facultyName

                    print("reading page {0}, faculty {1}, faculty code {2}".format(i, facultyName, facultyCode))
                except Exception as e:
                    print(e)
                    continue

    def updateExtraCourses(self):
        with open('ug-fetch/metadata/course_ids.txt') as file:
            rawCourses = file.readlines()
        courses = [CourseNum(x.strip()) for x in rawCourses]
        courseNums = [x for x in courses if x not in courses]
        print("adding {} classes".format(len(courseNums)))
        for courseNum in courseNums:
            self.manager.courses[courseNum] = Course(courseNum)
            faculty = courseNum.faculty()
            if faculty not in self.manager.faculties:
                print("adding faculty {}".format(faculty))
                self.manager.faculties[faculty] = Faculty(faculty, "")
            print("adding course {} to faculty {}".format(courseNum, faculty))
            self.manager.faculties[faculty].courses.append(courseNum)

    def updateExtraCoursesFromTxt(self):
        '''
        Get courses from extra files in the "txtPath" directory, and
        add them to the main Courses list, and the appropriate Faculty
        :return:
        '''
        for x in os.listdir(Paths.txtPath.value):
            path = os.path.join(Paths.txtPath.value, x)
            if os.path.isfile(path):
                print("got file ", path)
                with tempOpen(path, 'r') as file:
                    data = file.read()
                coursesNumbers = list(set(re.findall(courseRegex, data, re.DOTALL)))
                courseNumList = [CourseNum(x) for x in coursesNumbers]
                for courseNumber in courseNumList:
                    if courseNumber not in self.manager.courses:
                        self.manager.courses[courseNumber] = Course(courseNumber)
                        if courseNumber.faculty() not in self.manager.faculties:
                            raise AttributeError(
                                "Faculty with code " + courseNumber.faculty() + " not found in Faculties in catalogue!")
                        self.manager.faculties[courseNumber.faculty()].courses.append(courseNumber)

    # prune faculties with no courses on their page
    def pruneFaculties(self):
        for k in list(self.manager.faculties.keys()):
            if len(self.manager.faculties[k].courses) == 0:
                print("removing faculty {} because it has no courses".format(k))
                self.manager.faculties.pop(k, None)

    # def writeToFiles():
    #     toJSONFile(Faculties, Paths.jsonPath + "\\faculties.json")
    #     toJSONFile(Courses, Paths.jsonPath + "\\courses.json")
    #     toPickle(Faculties, Paths.picklePath + "\\faculties.p")
    #     toPickle(Courses, Paths.picklePath + "\\courses.p")

    def typoFixes(self):
        self.manager.courses.pop(self.manager.faculties['29'].courses[0])
        self.manager.courses.pop(self.manager.faculties['00'].courses[0])
        badCourses = {CourseNum(x) for x in {'294901', '03042'}}
        self.manager.faculties['21'].courses = [x for x in self.manager.faculties['21'].courses if x not in badCourses]
        self.manager.faculties.pop('29')
        self.manager.faculties.pop('00')
        self.manager.faculties['39'].name = 'קורסי ספורט'

    def writeToFiles(self):
        self.manager.writeToFiles()


if __name__ == "__main__":
    parser = txtParser()

    parser.parseTexts()
    parser.updateExtraCourses()
    parser.typoFixes()  # some errors in the catalogue, I remove them manually
    parser.pruneFaculties()
    parser.writeToFiles()

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
