import ghostscript  # for converting pdf file to text
from PyPDF2 import PdfFileReader  # just for getting number of pages in PDF
from bidi.algorithm import get_display

from utils import *

pdfFileName: str = r"Catalogue17-18.pdf"


# TODO: deprecate this function and the PyPDF2 dependency
def getPdfPageNum(fileName: str = pdfFileName) -> int:
    """
    tells us the number of pages in a pdf document,
    the document should be in the pdf directory as defined by
    pdfPath
    :param fileName:
    :return: the number of pages in that pdf file
    """
    pdfFile: str = Paths.pdfPath.value + fileName
    pdf = PdfFileReader(open(pdfFile, 'rb'))
    return pdf.getNumPages()


class pdfParser:
    pdfFile: str
    baseFileName: str
    targetDir: str

    def __init__(self, pdfFile: str = pdfFileName):
        self.pdfFile = pdfFile
        self.baseFileName = pdfFile.replace(".pdf", "")
        self.targetDir = os.path.join(Paths.txtPath.value, self.baseFileName)

    # TODO: wrap pdfParser and txtParser into one class so they save state - the name of the pdf file used for parsing
    def catalogueToTxtFiles(self) -> None:
        '''Parse the entire catalogue into text files (one for each page) using GhostScript:
        Note the %d which means each page becomes a different txt file
        :param:
        :return:
        '''
        # TODO: make txt file name depend on pdf name to parse multiple pdfs
        if not os.path.exists(self.targetDir):
            os.makedirs(self.targetDir)
        # os.mkdir(targerDir)
        # print(targerDir)
        args = [
            "gs".encode(),
            "-sDEVICE=txtwrite".encode(),
            # ("-o" + Paths.txtPath.value + "\\"
            #  + baseFileName + "\\" + baseFileName + r"-%d.txt").encode(),
            # ("-o" + targerDir + "\\" + baseFileName + r"-%d.txt").encode(),
            ("-o" + os.path.join(self.targetDir, self.baseFileName) + r"-%d.txt").encode(),
            # + FilenameConsts.FileName.value + r"%d" + FilenameConsts.Suffix.value).encode(),
            (Paths.pdfPath.value + "\\" + self.pdfFile).encode(),
        ]
        # with suppress_stdout():
        ghostscript.Ghostscript(*args)

    def reverseTextInFiles(self) -> None:
        """
        uses bidirectional algorithm's get_display method to reverse only RTL
        text, keeping English and numbers unchanged
        :return:
        """
        for file in os.scandir(self.targetDir):
            if not file.is_file():
                continue
            with open(file.path, "r+", encoding="utf8") as f:
                text = f.read()
                f.seek(0)
                f.write(get_display(text))
                f.truncate()
            print("updating file", file.name)


if __name__ == "__main__":
    parser = pdfParser()
    parser.catalogueToTxtFiles()
    parser.reverseTextInFiles()
