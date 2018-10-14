import os
from typing import Tuple

from pdfParser import pdfParser
from txtParser import txtParser
from dataManager import dataManager
from KdamClasses import FacultiesDB, CoursesDB
from utils import Paths, toJSONFile, toPickle, dictRecursiveFormat

pdfFilename: str = r"Catalogue17-18.pdf"


class pdfToDataParser:
    # baseFileName: str
    # targetDir: str
    pdfParser: pdfParser
    txtParser: txtParser
    dataManager: dataManager
    facFile = "faculties"
    courseFile = "courses"

    def __init__(self, pdf=None, txt=None, mgr=None, fromFiles=False, facultyFilePath: str = None,
                 courseFilePath: str = None):
        # self.baseFileName = pdfFileName.replace(".pdf", "")
        # self.targetDir = os.path.join(Paths.txtPath.value, self.baseFileName)
        self.pdfParser = pdf if pdf is not None else pdfParser()
        self.txtParser = txt if txt is not None else txtParser()
        self.dataManager = mgr if mgr is not None else dataManager(fromFiles, facultyFilePath, courseFilePath)

    def getDatabasesFromPdf(self, pdfFilename: str) -> Tuple[CoursesDB, FacultiesDB]:

        # if not accumulate:
        #     self.dataManager.purge()

        baseFilename = pdfFilename.replace(".pdf", "")
        targetDir = os.path.join(Paths.txtPath, baseFilename)
        # print(baseFilename)
        # print(Paths.txtPath.value)
        # print(targetDir)

        if not os.path.exists(targetDir):
            os.makedirs(targetDir)

        txtFilenameTemplate = os.path.join(targetDir, baseFilename) + r"-%03d.txt"
        print('converting pdf to txt files')
        self.pdfParser.catalogueToTxtFiles(txtFilenameTemplate, pdfFilename)
        print('reversing Hebrew text in txt files')
        self.pdfParser.reverseTextInFiles(targetDir)
        print('parsing text from text files')
        self.txtParser.parseTexts(self.dataManager, targetDir)
        self.txtParser.updateExtraCourses(self.dataManager)
        self.txtParser.typoFixes(self.dataManager)
        self.txtParser.pruneFaculties(self.dataManager)
        # self.txtParser.writeToFiles()
        # self.dataManager.writeToFiles()
        return self.dataManager.courses, self.dataManager.faculties

    def saveToFiles(self, courses: CoursesDB, faculties: FacultiesDB) -> None:
        toJSONFile(faculties, os.path.join(Paths.jsonPath, self.facFile + ".json"))
        # need to transform courseNum keys to strings, using dictRecursiveFormat
        toJSONFile(dictRecursiveFormat(courses), os.path.join(Paths.jsonPath, self.courseFile + ".json"))
        toPickle(faculties, os.path.join(Paths.picklePath, self.facFile + ".p"))
        toPickle(courses, os.path.join(Paths.picklePath, self.courseFile + ".p"))


if __name__ == "__main__":
    # lol = pdfToDataParser(fromFiles=True,
    #                       facultyFilePath=os.path.join(Paths.picklePath.value, pdfToDataParser.facFile),
    #                       courseFilePath=os.path.join(Paths.picklePath.value, pdfToDataParser.courseFile))

    lol = pdfToDataParser()
    # baseFilename = pdfFilename.replace(".pdf", "")
    # targetDir = os.path.join(Paths.txtPath.value, baseFilename)
    # print(baseFilename)
    # print(Paths.txtPath.value)
    # print(targetDir)

    # if not os.path.exists(targetDir):
    #     os.makedirs(targetDir)
    #
    # lol.txtParser.parseTexts(lol.dataManager, targetDir)
    lol.saveToFiles(*lol.getDatabasesFromPdf(pdfFilename))
