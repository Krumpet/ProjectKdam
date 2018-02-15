import ghostscript  # for converting pdf file to text (though Hebrew is reversed)\

from PyPDF2 import PdfFileReader  # just for getting number of pages in PDF
from utils import *

from utils import suppress_stdout  # so you don't see all of the output from Ghostscript

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

pdfFile = pdfPath + r"\Catalogue17-18.pdf"
pdf = PdfFileReader(open(pdfFile, 'rb'))
numOfPages: int = pdf.getNumPages()


def catalogueToTxtFiles():
    args = [
        "gs".encode(),
        "-sDEVICE=txtwrite".encode(),
        # ("-o" + "C:\\Users\\ADMIN\\PycharmProjects\\Project_Kdam\\data1\\blah-%d.txt").encode(),
        ("-o" + txtPath + "\\" + FileName + r"%d" + Suffix).encode(),
        pdfFile.encode(),
    ]
    # with suppress_stdout():
    ghostscript.Ghostscript(*args)


if __name__ == "__main__":
    catalogueToTxtFiles()
