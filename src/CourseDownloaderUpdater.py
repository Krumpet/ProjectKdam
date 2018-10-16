import re
import urllib.request as request
from collections import OrderedDict, deque
from typing import Set, Union, Deque, Tuple

from GraduateParser import parse_graduate
from KdamClasses import *
from utils import *


class CourseDownloaderUpdater:
    courses: CoursesDB
    faculties: FacultiesDB

    bad_online_courses: Set[CourseNum]

    hebrew = ['שם מקצוע', 'מספר מקצוע', 'אתר הקורס', 'נקודות',
              'הרצאה', 'תרגיל', 'מעבדה', 'סמינר/פרויקט', 'סילבוס', 'מקצועות זהים', 'מקצועות קדם', 'מקצועות צמודים',
              'מקצועות ללא זיכוי נוסף', 'מקצועות ללא זיכוי נוסף (מכילים)', 'מקצועות ללא זיכוי נוסף (מוכלים)',
              'עבור לסמסטר', 'אחראים', 'הערות', 'מועד הבחינה', 'מועד א', 'מועד ב', 'מיקום']
    irrelevant = 'move_to_semester in_charge comments exam_date exam_A exam_B location'.split()
    english = 'name id site points lecture tutorial lab project syllabus identical kdam adjacent no_more ' \
              'no_more_contains no_more_included'.split() + irrelevant
    trans = dict(zip(hebrew, english))

    def __init__(self, courses: CoursesDB = None, faculties: FacultiesDB = None):
        self.courses = from_pickle(Paths.pickleCourses) if courses is None else courses
        self.faculties = from_pickle(Paths.pickleFaculties) if faculties is None else faculties
        self.bad_online_courses = set()

    def download_and_update_courses(self):

        self.download_courses()
        self.update_followups_and_reverse_zamuds()

        print("found", len(self.bad_online_courses),
              "which are listed as kdams/zamuds but could not be found online. They will be removed from DB.")
        with open(Paths.bad_online_courses, 'w+') as file:
            print_in_lines(sorted(self.bad_online_courses), file=file)

        # courses that were in the pdf(s) we scanned but were not found online.
        # these could include typos.
        bad_catalogue_courses: Set[CourseNum] = {k for k, v in self.courses.items() if v.name == ""}
        print("found {} courses in the DB that were not found online. They will be removed from DB.".format(
            len(bad_catalogue_courses)))
        with open(Paths.bad_catalogue_courses, 'w+') as file:
            print_in_lines(sorted(bad_catalogue_courses), file=file)

        self.remove_courses(bad_catalogue_courses.union(self.bad_online_courses))

        to_pickle(self.faculties, Paths.pickleNewFaculties)
        to_pickle(self.courses, Paths.pickleNewCourses)

    def nested_string_list_to_course_nums(self, nested_list: List[List[str]]) -> List[List[CourseNum]]:
        return [[CourseNum(num) for num in sub_list] for sub_list in nested_list]

    def download_course(self, course: Union[CourseNum, Course]):
        try:
            real_course = course if isinstance(course, Course) else self.courses[course]
            # TODO: testing using courseNum as argument rather than ".cid"ing it
            info = self.fetch_course(real_course.courseId)
            if not info:  # meaning the course isn't on UG, try on graduate
                info = parse_graduate(real_course)
            real_course.name = info.get('name', "")
            if real_course.name == bad_course_on_grad:  # this means the course isn't on graduate
                real_course.name = ""

            # TODO: change these to sets
            real_course.kdams = self.nested_string_list_to_course_nums(info.get('kdam', []))
            real_course.zamuds = self.nested_string_list_to_course_nums(info.get('adjacent', []))

            real_course.moed_A = info.get('exam_A', "")
            real_course.moed_B = info.get('exam_B', "")
        except:
            pass

    def extract_info(self, html):
        div_fmt = r'<div class="{}">\s*(.*?)\s*</div>'
        keys = re.findall(div_fmt.format('property'), html)
        values = re.findall(div_fmt.format('property-value'), html)
        # print("found " + str(values))
        return OrderedDict(zip(keys, [re.sub('\s+', ' ', v) for v in values]))

    def fix(self, k, v):
        """
        kdam and adjacent are lists of lists, the rest are lists
        :param k:
        :param v:
        :return:
        """
        # TODO: fix exam dates so they're uniform with graduate parser
        data_title = r'data-original-title="(.*?)"'
        if k in ['kdam', 'adjacent']:
            return [re.findall(data_title, x) for x in v.split(' או ')]
        if k.startswith('no_more') or k in ['identical']:
            return re.findall(data_title, v)
        if k in ['site']:
            return re.search(r'href="(.*?)" ', v).group(1)
        if k in ['exam_A', 'exam_B']:
            return ".".join(re.search("\d{1,2}\.\d{1,2}\.\d{4}", v)[0].split(".")[0:2])
        return v

    def cleanup(self, raw_dict):
        od = OrderedDict((self.trans[k], self.fix(self.trans[k], v))
                         for k, v in raw_dict.items())
        if not od:
            return {}
        # TODO:
        if 'points' in od:
            od.move_to_end('points', last=False)
        od.move_to_end('id', last=False)
        if 'site' in od:
            od.move_to_end('site')
        od.move_to_end('syllabus')
        return od

    def fetch(self, url):
        with request.urlopen(url) as w:
            return w.read().decode('utf8')

    # TODO: use the address that includes semester and year
    def read_course(self, number: CourseNum):
        # return fetch("https://ug3.technion.ac.il/rishum/course/{}".format(number))
        return self.fetch(Addresses.TechnionUg + "{}".format(number))

    def fetch_course(self, number: CourseNum):
        return self.cleanup(self.extract_info(self.read_course(number)))

    def download_courses(self):
        print("downloading data for courses:")
        for i, course_id in enumerate(self.courses):
            print(str(i + 1), "/", len(self.courses), " [{}]".format(course_id))
            self.download_course(course_id)

    def update_followups_and_reverse_zamuds(self):
        # TODO: handle updating faculties when a new course is discovered
        courses_to_check: Deque[Tuple[CourseNum, Course]] = deque(self.courses.items())
        attributes_and_opposites = {'kdams': 'followups', 'zamuds': 'reverseZamuds'}
        while courses_to_check:
            cid, course = courses_to_check.popleft()
            # if this is a course discovered while updating kdams/zamuds, add to courses
            if cid not in self.courses:
                self.courses[cid] = course
            # go over the courses kdams/zamuds and update the opposite direction
            # if we discover a course not in Courses, create it and add it to the end of the queue
            for attr in attributes_and_opposites.keys():
                main_list: List[List[CourseNum]] = getattr(course, attr)
                for sublist in main_list:
                    for k_or_z_id in sublist:
                        if k_or_z_id in self.courses:  # the simple case
                            opposite_attribute: List[CourseNum] = getattr(self.courses[k_or_z_id],
                                                                          attributes_and_opposites[attr])

                            opposite_attribute.append(cid)
                        else:
                            # we've found a course that doesn't exist.
                            # if it hasn't been discovered already, create it,
                            # and append to courses_to_check

                            # test if this course id is already in the queue
                            # if so, update it
                            if k_or_z_id in {k[0] for k in
                                             courses_to_check}:
                                # finding an item in the queue is ugly
                                course_to_update: Course = \
                                    list(filter(lambda tup: tup[0] == k_or_z_id, courses_to_check))[0][1]
                                opposite_attribute: List[CourseNum] = getattr(course_to_update,
                                                                              attributes_and_opposites[attr])
                                opposite_attribute.append(cid)
                                continue
                            # if we've discovered it and know it's a bad course, disregard and more on
                            elif k_or_z_id in self.bad_online_courses:
                                continue
                            # we're encountering the course for the first time
                            else:
                                new_course = Course(k_or_z_id)
                                self.download_course(new_course)
                                # some stuff here will change once Faculties and Courses are default key dicts
                                print("found course not in catalogue for the first time -", k_or_z_id, end=" ")
                                if new_course.name == "":
                                    print("could not find it online, it will not be included in DB")
                                    self.bad_online_courses.add(k_or_z_id)
                                    continue
                                else:
                                    print("found the data online -", new_course.name)
                                    courses_to_check.append((k_or_z_id, new_course))
                                    opposite_attribute: List[CourseNum] = getattr(new_course,
                                                                                  attributes_and_opposites[attr])
                                    opposite_attribute.append(cid)

    def remove_courses(self, bad_courses: Iterable[CourseNum]) -> None:
        # remove from zamud lists
        for courseId, course in self.courses.items():
            for zamudList in course.zamuds:
                for zamud in zamudList:
                    if zamud in bad_courses:
                        zamudList.remove(zamud)
                        if not zamudList:
                            course.zamuds.remove(zamudList)

        # remove from kdam lists
        for courseId, course in self.courses.items():
            for kdamList in course.kdams:
                for kdam in kdamList:
                    if kdam in bad_courses:
                        kdamList.remove(kdam)
                        if not kdamList:
                            course.kdams.remove(kdamList)

        # remove from faculty course list
        # TODO: change to set
        for facultyCode, faculty in self.faculties.items():
            faculty.courses = [x for x in faculty.courses if x not in bad_courses]

        for course in bad_courses:
            self.courses.pop(course, None)

        # prune faculties with no courses on their page
        self.faculties = {k: v for k, v in self.faculties.items() if v.courses}


if __name__ == "__main__":
    downloader = CourseDownloaderUpdater()
    downloader.download_and_update_courses()

    # def getEncoding(data):
    #     """
    #     receives byes of data from opening HTML file,
    #     returns the appropriate codec i.e 'utf-8' or 'windows-1255'
    #     :param data:
    #     :return:
    #     """
    #     return re.findall(r"(?i)charset=\"?([^\s]+)\"", str(data))[0]

    # def getHtmlDataFromURL(url: str):
    #     f = urlopen(url)
    #     return f.read()
    #
    #
    # def getHTMLDataFromUG(courseId: CourseNum):
    #     return getHtmlDataFromURL(Addresses.TechnionUg + str(courseId))
    #
    #
    # def getHTMLDataFromGrad(courseId: CourseNum):
    #     return getHtmlDataFromURL(Addresses.TechnionGrad + str(courseId))

    # def parseDataFromGraduate(data, courseId):
    #     pass

    # def listSubFaculties():
    #     result = sorted(list(set([coursenum[:3] for coursenum in Courses])))
    #     print("subfaculties: ", result)
    #     return result

    # def listAllCourses():
    #     List = []
    #     for subfaculty in listSubFaculties():
    #         List.extend([subfaculty + str(num).zfill(3) for num in range(1000)])
    #
    #         # if len(faculty) == 2:
    #         #     List.extend([faculty + digit + str(num).zfill(3) for num in range(1000) for digit in ThirdDigit])
    #         # elif len(faculty) == 3:
    #         #     List.extend([faculty + str(num).zfill(3) for num in range(1000)])
    #     # print(List[:100])
    #     return List

    # def courseOnUg(courseId):
    #     # print("trying course " + str(courseId))
    #     data = getHTMLDataFromUG(courseId)
    #     strData = str(data, encoding='utf8')
    #     # if not (len(re.findall("לא קיים", strData)) > 0):
    #     #     print("===ON UG===")
    #     # else:
    #     #     print("===NOT ON UG===")
    #     return not (len(re.findall("לא קיים", strData)) > 0)

    # def update_followups():
    #     for courseId, course in Courses.items():
    #         for kdamList in course.kdams:
    #             for kdam in kdamList:
    #                 # if kdam in Courses:
    #                 #     Courses[kdam].followups.append(courseId)
    #                 if kdam not in Courses:
    #                     print(kdam, "not found in courses", end=" ")
    #                     # handle adding a new course
    #                     new_course = Course(kdam)
    #                     download_course(new_course)
    #                     # some stuff here will change once Faculties and Courses are default key dicts
    #                     # print(new_course.name, 'is the name I found')
    #                     if new_course.name == "":
    #                         print('or online, this bad course will be removed')
    #                         courses_not_found.add(kdam)
    #                         continue
    #                     print('but found online, adding this course to the dictionary')
    #                     courses_not_in_catalogue.add(kdam)
    #                 else:
    #                     Courses[kdam].followups.append(courseId)
    #
    #     for courseId, course in Courses.items():
    #         course.followups = list(set(course.followups))
    #
    #
    # def update_reverse_zamuds():
    #     for courseId, course in Courses.items():
    #         for zamudList in course.zamuds:
    #             for zamud in zamudList:
    #                 if zamud in Courses:
    #                     Courses[zamud].reverseZamuds.append(courseId)
    #                 else:
    #                     print(zamud, str(zamud), "not found in courses")
    #                     courses_not_in_catalogue.add(zamud)
    #
    #     for courseId, course in Courses.items():
    #         course.reverseZamuds = list(set(course.reverseZamuds))

    # for course in Courses:
    #     getCourseInfo(course)

    # # in case some files are not included in Courses:
    # for x in os.listdir(htmlPath):
    #     if os.path.isfile(os.path.join(htmlPath, x)):
    #         courseId = CourseNum(os.path.splitext(x)[0])
    #         Faculties[courseId.faculty()].courses.append(courseId)
    #
    #         Courses[courseId] = Course(courseId)
    #         getCourseInfo(courseId)

    # print(Courses[CourseNum("234123")].followups)
    # print(Courses[CourseNum("234123")].kdams)
    # print(Courses[CourseNum("234123")].zamuds)
    # print(Courses[CourseNum("234123")].name)

    # def getZamuds(data):
    #     try:
    #         zamuds = list(set(re.findall(courseRegex, re.findall("מקצועות צמודים.*?/div><div", data, re.DOTALL)[0])))
    #         zamuds = list(set([CourseNum(x).id for x in zamuds]))
    #     except:
    #         zamuds = []
    #     return zamuds

    # def getSubject(data):
    #     try:
    #         subject = re.findall("\|.*\|(.*)</title>", data)[0].strip()
    #     except:
    #         subject = "None"
    #     return subject

    # def getExams(data: str) -> List[str]:
    #     exams: List[str] = re.findall(">.*(\d\d\.\d\d).*" + Semester.TestYear, data)
    #
    #     if (len(exams) > 1):
    #         return exams[:2]
    #     elif (len(exams) == 1):
    #         return [exams[0], ""]
    #     else:
    #         return ["", ""]

    # def getCourseInfo(courseId):
    #     path = htmlPath + "\\" + str(courseId) + ".htm"
    #     try:
    #         with open(path, mode='r', encoding='utf8') as file:
    #             strData = file.read()
    #             Courses[courseId].name = getSubject(strData)
    #             Courses[courseId].kdams = getKdams(strData)
    #             Courses[courseId].zamuds = getZamuds(strData)
    #             Courses[courseId].moed_A, Courses[courseId].moed_B = getExams(strData)
    #     except UnicodeDecodeError:
    #         with open(path, mode='r', encoding='windows-1255') as file:
    #             strData = file.read()
    #             htmlParser = MyHTMLParser()
    #             htmlParser.feed(strData)
    #             Courses[courseId].name = htmlParser.name
    #     finally:
    #         os.remove(path)

    # def getKdams(data):
    #     try:
    #         kdams = list(set(re.findall(courseRegex, re.findall("מקצועות קדם.*?/div><div", data, re.DOTALL)[0])))
    #         kdams = list(set([CourseNum(x).id for x in kdams]))
    #     except:
    #         kdams = []
    #     return kdams

    # Faculties: FacultiesDB = from_pickle(Paths.pickleFaculties)
    # Courses: CoursesDB = from_pickle(Paths.pickleCourses)
    # Courses: CoursesDB = from_pickle(Paths.pickleNewCourses)

    # courses listed online as kdam/zamud of another course,
    # but don't exist online.

    # update_courses()

    # update_followups()
    # update_reverse_zamuds()
    # update_followups_and_reverse_zamuds()

    # print(
    #     "found {} courses listed as kdam/zamud listed only on Graduate, not included in database, writing to "
    #     "graduate_only_courses.txt".format(
    #         len(courses_not_in_catalogue)))
    # print("found", len(bad_online_courses),
    #       "which are listed as kdams/zamuds but could not be found online. They will be removed from DB.")
    # with open(Paths.bad_online_courses, 'w+') as file:
    #     print_in_lines(sorted(bad_online_courses), file=file)
    #
    # # typoCourses = [k for k, v in Courses.items() if v.name == bad_course_on_grad]
    #
    # # courses that were in the pdf(s) we scanned but were not found online.
    # # these could include typos.
    # bad_catalogue_courses: Set[CourseNum] = {k for k, v in Courses.items() if v.name == ""}
    # print("found {} courses in the DB that were not found online. They will be removed from DB.".format(
    #     len(bad_catalogue_courses)))
    # with open(Paths.bad_catalogue_courses, 'w+') as file:
    #     print_in_lines(sorted(bad_catalogue_courses), file=file)
    #
    # Faculties = remove_courses(bad_catalogue_courses.union(bad_online_courses), faculties=Faculties, courses_db=Courses)
    #
    # to_pickle(Faculties, Paths.pickleNewFaculties)
    # to_pickle(Courses, Paths.pickleNewCourses)

    # Faculties = prune_faculties(Faculties)

    # testCourses = ['234123','236335']
    # for x in testCourses:
    #     downloadCourse(x)

    # info = fetch_course('234123')
    # print(info)
    # moed_A = info.get('exam_A', "")
    # moed_A_split = moed_A.split('.')
    # moed_A_re = re.search("\d{1,2}\.\d{1,2}\.\d{4}", info['exam_A'])
    # # print(moed_A_re[0].split(".")[0:2])
    # print(".".join(moed_A_re[0].split(".")[0:2]))
    # print(moed_A_re[0])
    # print(moed_A)
    # print(moed_A_split)

    # info2 = fetch_course("238739")
    # print(info2)
    # print(listAllCourses())
    # megalist = listAllCourses()
    # print("length of megalist = " + str(len(megalist)))
    # filteredlist = filter(lambda x: courseOnUg(x) and CourseNum(x) not in Courses.keys(), megalist)
    # print(list(filteredlist))
