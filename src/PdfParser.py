import os

import ghostscript  # for converting pdf file to text
from bidi.algorithm import get_display

from Consts import Paths


class PdfParser:

    @staticmethod
    def catalogue_to_txt_files(txt_filename_template, pdf_filename) -> None:
        """
        Parse the entire catalogue into text files (one for each page) using GhostScript:
        Note the %d which means each page becomes a different txt file
        :param:
        :return:
        """

        args = list(map(lambda s: s.encode(),  # args need to be encoded into bytes
                        [
                            "gs",  # name of the command
                            "-sDEVICE=txtwrite",  # job type - writing to txt files
                            "-o" + txt_filename_template,  # output filename template
                            os.path.join(Paths.PDF_PATH, pdf_filename),  # input filename
                        ]))

        # with suppress_stdout():
        ghostscript.Ghostscript(*args)

    @staticmethod
    def reverse_text_in_files(target_dir) -> None:
        """
        uses bidirectional algorithm's get_display method to reverse only RTL
        text, keeping English and numbers unchanged
        :return:
        """
        for dir_entry in os.scandir(target_dir):
            if not dir_entry.is_file():
                continue
            with open(dir_entry.path, "r+", encoding="utf8") as file:
                text = file.read()
                file.seek(0)
                file.write(get_display(text))
                file.truncate()
            print("updating file", dir_entry.name)

# if __name__ == "__main__":
# parser = pdfParser()
# parser.catalogueToTxtFiles()
# parser.reverseTextInFiles()

# def getPdfPageNum(fileName: str) -> int:
#     """
#     tells us the number of pages in a pdf document,
#     the document should be in the pdf directory as defined by
#     pdfPath
#     :param fileName:
#     :return: the number of pages in that pdf file
#     """
#     pdfFile: str = os.path.join(Paths.pdfPath, fileName)
#     pdf = PdfFileReader(open(pdfFile, 'rb'))
#     return pdf.getNumPages()
