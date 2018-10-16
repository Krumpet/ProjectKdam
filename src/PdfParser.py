import ghostscript  # for converting pdf file to text
# from PyPDF2 import PdfFileReader  # just for getting number of pages in PDF
from bidi.algorithm import get_display

from utils import *


# TODO: deprecate this function and the PyPDF2 dependency
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


class PdfParser:
    # pdfFile: str
    # baseFileName: str
    # targetDir: str

    # def __init__(self):
    #
    #         # self.pdfFile = pdfFile
    #     # # TODO: extract both of these to the upper manager
    #     # self.baseFileName = pdfFile.replace(".pdf", "")
    #     # self.targetDir = os.path.join(Paths.txtPath.value, self.baseFileName)

    # TODO: wrap pdfParser and txtParser into one class so they save state - the name of the pdf file used for parsing
    @staticmethod
    def catalogue_to_txt_files(txt_filename_template, pdf_filename) -> None:
        """
        Parse the entire catalogue into text files (one for each page) using GhostScript:
        Note the %d which means each page becomes a different txt file
        :param:
        :return:
        """
        # TODO: make txt file name depend on pdf name to parse multiple pdfs
        # if not os.path.exists(self.targetDir):
        #     os.makedirs(self.targetDir)
        # os.mkdir(targerDir)
        # print(targerDir)
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
        for file in os.scandir(target_dir):
            if not file.is_file():
                continue
            with open(file.path, "r+", encoding="utf8") as f:
                text = f.read()
                f.seek(0)
                f.write(get_display(text))
                f.truncate()
            print("updating file", file.name)

# if __name__ == "__main__":
# parser = pdfParser()
# parser.catalogueToTxtFiles()
# parser.reverseTextInFiles()
