import os
from typing import Tuple

from PdfParser import PdfParser
from TxtParser import TxtParser
from DataManager import DataManager
from KdamClasses import FacultiesDB, CoursesDB
from utils import Paths, to_json_file, to_pickle, dict_recursive_format

pdfFilename: str = r"Catalogue17-18.pdf"


class PdfToDataParser:
    # baseFileName: str
    # targetDir: str
    pdfParser: PdfParser
    txtParser: TxtParser
    dataManager: DataManager
    facFile = "faculties"
    courseFile = "courses"

    def __init__(self, pdf=None, txt=None, mgr=None, from_files=False, faculty_file_path: str = None,
                 course_file_path: str = None) -> None:
        # self.baseFileName = pdfFileName.replace(".pdf", "")
        # self.targetDir = os.path.join(Paths.txtPath.value, self.baseFileName)
        self.pdfParser = pdf if pdf is not None else PdfParser()
        self.txtParser = txt if txt is not None else TxtParser()
        self.dataManager = mgr if mgr is not None else DataManager(from_files, faculty_file_path, course_file_path)

    def get_databases_from_pdf(self, pdf_filename: str) -> Tuple[CoursesDB, FacultiesDB]:

        # if not accumulate:
        #     self.dataManager.purge()

        base_filename = pdf_filename.replace(".pdf", "")
        target_dir = os.path.join(Paths.txtPath, base_filename)
        # print(base_filename)
        # print(Paths.txtPath.value)
        # print(target_dir)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        txt_filename_template = os.path.join(target_dir, base_filename) + r"-%03d.txt"
        print('converting pdf to txt files')
        self.pdfParser.catalogue_to_txt_files(txt_filename_template, pdf_filename)
        print('reversing Hebrew text in txt files')
        self.pdfParser.reverse_text_in_files(target_dir)
        print('parsing text from text files')
        self.txtParser.parse_texts(self.dataManager, target_dir)
        self.txtParser.update_extra_courses(self.dataManager)
        self.txtParser.typo_fixes(self.dataManager)
        self.txtParser.prune_faculties(self.dataManager)
        # self.txtParser.writeToFiles()
        # self.dataManager.writeToFiles()
        return self.dataManager.courses, self.dataManager.faculties

    def save_to_files(self, courses: CoursesDB, faculties: FacultiesDB) -> None:
        to_json_file(faculties, os.path.join(Paths.jsonPath, self.facFile + ".json"))
        # need to transform courseNum keys to strings, using dictRecursiveFormat
        to_json_file(dict_recursive_format(courses), os.path.join(Paths.jsonPath, self.courseFile + ".json"))
        to_pickle(faculties, os.path.join(Paths.picklePath, self.facFile + ".p"))
        to_pickle(courses, os.path.join(Paths.picklePath, self.courseFile + ".p"))


if __name__ == "__main__":
    # lol = pdfToDataParser(fromFiles=True,
    #                       facultyFilePath=os.path.join(Paths.picklePath.value, pdfToDataParser.facFile),
    #                       courseFilePath=os.path.join(Paths.picklePath.value, pdfToDataParser.courseFile))

    lol = PdfToDataParser()
    # baseFilename = pdfFilename.replace(".pdf", "")
    # targetDir = os.path.join(Paths.txtPath.value, baseFilename)
    # print(baseFilename)
    # print(Paths.txtPath.value)
    # print(targetDir)

    # if not os.path.exists(targetDir):
    #     os.makedirs(targetDir)
    #
    # lol.txtParser.parseTexts(lol.dataManager, targetDir)
    lol.save_to_files(*lol.get_databases_from_pdf(pdfFilename))
