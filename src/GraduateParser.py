from utils import *
from typing import Dict, Match
from KdamClasses import *
import xml.etree.ElementTree as ET
from lxml import etree
import urllib.request as request

backupPath = htmlPath + r"\backup html"

categories = ['מקצועות זהים', 'מקצועות קדם', 'מקצועות צמודים', 'מקצועות ללא זיכוי נוסף',
              'מקצועות ללא זיכוי נוסף (מכילים)', 'מקצועות ללא זיכוי נוסף (מוכלים)', 'מקצועות מכילים']
english = 'identical kdam adjacent no_more no_more_contains no_more_included contains'.split()
trans = dict(zip(categories, english))


def parseGraduate(courseId):
    # categories = ['מקצועות קדם', 'מקצועות צמודים', 'מקצועות ללא זיכוי נוסף', 'מקצועות ללא זיכוי נוסף (מוכלים)']

    w = request.urlopen(TechnionGrad + courseId)
    htm = w.read().decode('windows-1255')
    # print(htm)
    # parser = ET.XMLParser(encoding='windows-1255')
    # parser = ET.XMLParser(encoding='latin-1')

    # tree = ET.parse(backupPath + "\\" + "testphysics" + ".htm", parser=parser)

    # tree = ET.parse(htm, parser=parser)
    # root: ET.Element = tree.getroot()

    root = etree.fromstring(htm)  # , parser=parser)
    dataDictionary = {}
    titleElement = root.findall(".//title")
    if titleElement:
        data = titleElement[0].text
        title = "-".join(data.split(":")[1].split("-")[:-1]).strip()
        dataDictionary['name'] = title

    testElements = root.findall(".//*[@class='tab1']/tr/td")
    testRegex = re.compile("\d{1,2}\.\d{1,2}\.\d{4}")
    dateList = list(filter(testRegex.match, [element.text.strip() for element in testElements]))
    if dateList:
        dataDictionary['exam_A'] = ".".join(dateList[0].split('.')[0:2])
        if len(dateList) > 1:
            dataDictionary['exam_B'] = ".".join(dateList[1].split('.')[0:2])

    elements = root.findall(".//*[@class='tab0']/tr")
    Lines = []
    for element in elements:
        Line = []
        # TODO: write recursive helper function with depth 3
        if element.text.strip() != "":
            Line.append(element.text.strip())
            # print(element.text.strip())
        for subelement in element.getchildren():
            if subelement.text.strip() != "":
                Line.append(subelement.text.strip())
            for subsubelement in subelement.getchildren():
                if subsubelement.text.strip() != "":
                    Line.append(subsubelement.text.strip())
        Lines.append(Line)

    currentKey = ""  # category we are reading now, 'kdam', 'zamud', etc
    # print(Lines)
    for line in Lines:
        if not line:
            continue
        if line[-1] in categories:  # start reading new category
            currentKey = trans[line[-1]]
            currentList = []
            dataDictionary[currentKey] = []
            dataDictionary[currentKey].append(currentList)
        if line[-1] == 'או':  # same category, new list of possible kdams
            currentList = []
            dataDictionary[currentKey].append(currentList)
        r = re.compile("\d{5,6}")
        newlist = filter(r.match, line)
        course = CourseNum(list(newlist)[0])
        currentList.append(course)  # This is declared depending on the start of the line, and should always be valid

    # Currently only kdam and adjacent are lists of lists, the others need to be extracted
    # TODO: split all lists in categories[2:] instead of 2,3 manually
    for category in english:
        if category in ['kdam', 'adjacent']:
            continue
        if category in dataDictionary:
            dataDictionary[category] = dataDictionary[category][0]

    # if categories[2] in dataDictionary:
    #     dataDictionary[categories[2]] = dataDictionary[categories[2]][0]
    # if categories[3] in dataDictionary:
    #     dataDictionary[categories[3]] = dataDictionary[categories[3]][0]

    print(courseId + " : " + str(dataDictionary))

    return dataDictionary

# info = parseGraduate('234123')
# info = fetch_course('234123')
# print(info)

# courseNum = "236335"
# courseNum = "114074"

# graduateCourseRegex = "(?:(?P<kdams>.*?)מקצועות קדם)?(?:(?P<zamuds>.*?)מקצועות צמודים)?(?:(?P<noZikui>.*?)מקצועות ללא זיכוי נוסף)?(?:(?P<Moohal>.*?)מקצועות ללא זיכוי נוסף \(מוכלים)?(?P<extra>.*)"

# parseGraduate(courseNum)
