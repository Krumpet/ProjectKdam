import os
from typing import Tuple

from pdfParser import pdfParser
from txtParser import txtParser
from dataManager import CoursesDB, FacultiesDB, dataManager
from utils import Paths, toJSONFile, toPickle

pdfFileName: str = r"Catalogue17-18.pdf"


class pdfToDataParser:
    # baseFileName: str
    # targetDir: str
    pdfParser: pdfParser
    txtParser: txtParser
    dataManager: dataManager
    facFile = "faculties.p"
    courseFile = "courses.p"

    def __init__(self, pdf=None, txt=None, mgr=None):
        # self.baseFileName = pdfFileName.replace(".pdf", "")
        # self.targetDir = os.path.join(Paths.txtPath.value, self.baseFileName)
        self.pdfParser = pdf if pdf is not None else pdfParser()
        self.txtParser = txt if txt is not None else txtParser()
        self.dataManager = mgr if mgr is not None else dataManager()

    def getDatabasesFromPdf(self, pdfFilename: str, accumulate: bool = False) -> Tuple[CoursesDB, FacultiesDB]:

        if not accumulate:
            self.dataManager.purge()

        baseFilename = pdfFilename.replace(".pdf", "")
        targetDir = os.path.join(Paths.txtPath.value, baseFilename)

        if not os.path.exists(targetDir):
            os.makedirs(targetDir)

        txtFilenameTemplate = os.path.join(targetDir, baseFilename) + r"-%d.txt"
        self.pdfParser.catalogueToTxtFiles(txtFilenameTemplate, pdfFilename)
        self.pdfParser.reverseTextInFiles(targetDir)
        self.txtParser.parseTexts(self.dataManager, targetDir)
        # self.txtParser.updateExtraCourses()
        # self.txtParser.pruneFaculties()
        # self.txtParser.writeToFiles()
        # self.dataManager.writeToFiles()
        return self.dataManager.courses, self.dataManager.faculties

    def saveToFiles(self, courses, faculties) -> None:
        toJSONFile(faculties, os.path.join(Paths.jsonPath.value, self.facFile))
        toJSONFile(courses, os.path.join(Paths.jsonPath.value, self.courseFile))
        toPickle(faculties, os.path.join(Paths.picklePath.value, self.facFile))
        toPickle(courses, os.path.join(Paths.picklePath.value, self.courseFile))
