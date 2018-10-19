import os
from typing import Tuple

from PdfParser import PdfParser
from TxtParser import TxtParser
from DataManager import DataManager
from KdamClasses import FacultiesDB, CoursesDB
from Utils import to_json_file, to_pickle, dict_recursive_format
from Consts import Paths

pdfFilename: str = r"Catalogue17-18.pdf"


class PdfToDataParser:
    # baseFileName: str
    # targetDir: str
    pdf_parser: PdfParser
    txt_parser: TxtParser
    data_manager: DataManager
    facFile = "faculties"
    courseFile = "courses"

    def __init__(self, pdf=None, txt=None, mgr=None, from_files=False, faculty_file_path: str = None,
                 course_file_path: str = None) -> None:
        # self.baseFileName = pdfFileName.replace(".pdf", "")
        # self.targetDir = os.path.join(Paths.txtPath.value, self.baseFileName)
        self.pdf_parser = pdf if pdf is not None else PdfParser()
        self.txt_parser = txt if txt is not None else TxtParser()
        self.data_manager = mgr if mgr is not None else DataManager(from_files, faculty_file_path, course_file_path)

    def get_databases_from_pdf(self, pdf_filename: str) -> Tuple[CoursesDB, FacultiesDB]:
        # if not accumulate:
        #     self.dataManager.purge()

        base_filename = pdf_filename.replace(".pdf", "")
        target_dir = os.path.join(Paths.TXT_PATH, base_filename)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        txt_filename_template = os.path.join(target_dir, base_filename) + r"-%03d.txt"
        print('converting pdf to txt files')
        self.pdf_parser.catalogue_to_txt_files(txt_filename_template, pdf_filename)
        print('reversing Hebrew text in txt files')
        self.pdf_parser.reverse_text_in_files(target_dir)
        print('parsing text from text files')
        self.txt_parser.parse_texts(self.data_manager, target_dir)
        self.txt_parser.update_extra_courses(self.data_manager)
        self.txt_parser.typo_fixes(self.data_manager)

        return self.data_manager.courses, self.data_manager.faculties

    def save_to_files(self, courses: CoursesDB, faculties: FacultiesDB) -> None:
        to_json_file(faculties, os.path.join(Paths.JSON_PATH, self.facFile + ".json"))
        # need to transform courseNum keys to strings, using dictRecursiveFormat
        to_json_file(dict_recursive_format(courses), os.path.join(Paths.JSON_PATH, self.courseFile + ".json"))
        to_pickle(faculties, os.path.join(Paths.PICKLE_PATH, self.facFile + ".p"))
        to_pickle(courses, os.path.join(Paths.PICKLE_PATH, self.courseFile + ".p"))


def main():
    lol = PdfToDataParser()
    lol.save_to_files(*lol.get_databases_from_pdf(pdfFilename))


if __name__ == "__main__":
    main()
