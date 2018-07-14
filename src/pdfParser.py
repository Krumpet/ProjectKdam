from os import DirEntry

import ghostscript  # for converting pdf file to text (though Hebrew is reversed)\
from PyPDF2 import PdfFileReader  # just for getting number of pages in PDF
from bidi.algorithm import get_display
from utils import *


# p=pdf.getPage(70)
#
# p_text= p.extractText()
# # extract data line by line
# P_lines=[line for line in p_text.splitlines() if line!='']
# print(P_lines)

# getPageNum = [
#     "gs".encode(),
#     "-q".encode(), "-dNODISPLAY".encode(),
#     "-c".encode() + "(C:\\Users\\ADMIN\\PycharmProjects\\Project_Kdam\\data1\\Catalogue17-18.pdf) (r) file runpdfbegin pdfpagecount = quit".encode()
# ]
#
# ghostscript.Ghostscript(*getPageNum)
# TODO: extract to consts

def getPdfPageNum(fileName: str) -> int:
    pdfFile: str = Paths.pdfPath.value + fileName
    pdf = PdfFileReader(open(pdfFile, 'rb'))
    return pdf.getNumPages()


pdfFileName: str = Paths.pdfPath.value + r"\Catalogue17-18.pdf"


# pdf = PdfFileReader(open(pdfFile, 'rb'))
# numOfPages: int = getPdfPageNum(pdfFile)


# pdf.getNumPages()


def catalogueToTxtFiles(pdfFile: str = pdfFileName):
    args = [
        "gs".encode(),
        "-sDEVICE=txtwrite".encode(),
        # ("-o" + "C:\\Users\\ADMIN\\PycharmProjects\\Project_Kdam\\data1\\blah-%d.txt").encode(),
        (
                "-o" + Paths.txtPath.value + "\\" + FilenameConsts.FileName.value + r"%d" + FilenameConsts.Suffix.value).encode(),
        pdfFile.encode(),
    ]
    # with suppress_stdout():
    ghostscript.Ghostscript(*args)


def reverseTextInFiles():
    for file in os.scandir(Paths.txtPath.value):
        if not file.is_file():
            continue
        path = file.path
        with open(path, "r+", encoding="utf8") as f:
            text = f.read()
            # lines = f.readlines()
            f.seek(0)

            f.write(get_display(text))

            # lines = [line[::-1] for line in lines]
            # f.writelines(lines)

            f.truncate()
        print("updating file ", path)
        # TODO: reverse text in each line and save to original file
        # current implementation reversed everything including numbers and English


if __name__ == "__main__":
    catalogueToTxtFiles()
    reverseTextInFiles()
