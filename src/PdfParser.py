import os

import ghostscript  # for converting pdf file to text
from bidi.algorithm import get_display

from Utils import Paths


class PdfParser:

    @staticmethod
    def catalogue_to_txt_files(txt_filename_template, pdf_filename) -> None:
        """
        Parse the entire catalogue into text files (one for each page) using GhostScript:
        Note the %d which means each page becomes a different txt file
        :param:
        :return:
        """

        # TODO: map encode over the strings
        print(os.path.join(Paths.pdfPath, pdf_filename))
        args = [
            "gs".encode(),
            "-sDEVICE=txtwrite".encode(),
            # ("-o" + Paths.txtPath.value + "\\"
            #  + baseFileName + "\\" + baseFileName + r"-%d.txt").encode(),
            # ("-o" + targerDir + "\\" + baseFileName + r"-%d.txt").encode(),
            ("-o" + txt_filename_template).encode(),
            # + FilenameConsts.FileName.value + r"%d" + FilenameConsts.Suffix.value).encode(),
            # (Paths.pdfPath.value + "\\" + pdfFilename).encode(),
            (os.path.join(Paths.pdfPath, pdf_filename)).encode(),
        ]
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
