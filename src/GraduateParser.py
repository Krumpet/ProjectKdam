import re
import urllib.request as request

from lxml import etree

from KdamClasses import *
from utils import *

backupPath = Paths.htmlPath + r"\backup html"

categories = ['מקצועות זהים', 'מקצועות קדם', 'מקצועות צמודים', 'מקצועות ללא זיכוי נוסף',
              'מקצועות ללא זיכוי נוסף (מכילים)', 'מקצועות ללא זיכוי נוסף (מוכלים)', 'מקצועות מכילים']
english = 'identical kdam adjacent no_more no_more_contains no_more_included contains'.split()
trans = dict(zip(categories, english))


def parse_graduate(course_id):
    # categories = ['מקצועות קדם', 'מקצועות צמודים', 'מקצועות ללא זיכוי נוסף', 'מקצועות ללא זיכוי נוסף (מוכלים)']

    w = request.urlopen(Addresses.TechnionGrad + course_id)
    htm = w.read().decode('windows-1255')
    # print(htm)
    # parser = ET.XMLParser(encoding='windows-1255')
    # parser = ET.XMLParser(encoding='latin-1')

    # tree = ET.parse(backupPath + "\\" + "testphysics" + ".htm", parser=parser)

    # tree = ET.parse(htm, parser=parser)
    # root: ET.Element = tree.getroot()

    root = etree.fromstring(htm)  # , parser=parser)
    data_dictionary = {}
    title_element = root.findall(".//title")
    if title_element:
        data = title_element[0].text
        title = "-".join(data.split(":")[1].split("-")[:-1]).strip()
        data_dictionary['name'] = title

    test_elements = root.findall(".//*[@class='tab1']/tr/td")
    test_regex = re.compile("\d{1,2}\.\d{1,2}\.\d{4}")
    date_list = list(filter(test_regex.match, [element.text.strip() for element in test_elements]))
    if date_list:
        data_dictionary['exam_A'] = ".".join(date_list[0].split('.')[0:2])
        if len(date_list) > 1:
            data_dictionary['exam_B'] = ".".join(date_list[1].split('.')[0:2])

    elements = root.findall(".//*[@class='tab0']/tr")
    lines = []
    for element in elements:
        line = []
        # TODO: write recursive helper function with depth 3
        if element.text.strip() != "":
            line.append(element.text.strip())
            # print(element.text.strip())
        for subelement in element.getchildren():
            if subelement.text.strip() != "":
                line.append(subelement.text.strip())
            for subsubelement in subelement.getchildren():
                if subsubelement.text.strip() != "":
                    line.append(subsubelement.text.strip())
        lines.append(line)

    current_key = ""  # category we are reading now, 'kdam', 'zamud', etc
    # print(lines)
    for line in lines:
        if not line:
            continue
        current_list = []
        if line[-1] in categories:  # start reading new category
            current_key = trans[line[-1]]
            current_list = []
            data_dictionary[current_key] = []
            data_dictionary[current_key].append(current_list)
        if line[-1] == 'או':  # same category, new list of possible kdams
            current_list = []
            data_dictionary[current_key].append(current_list)
        r = re.compile("\d{5,6}")
        newlist = filter(r.match, line)
        course = CourseNum(list(newlist)[0])
        current_list.append(course)  # This is declared depending on the start of the line, and should always be valid

    # Currently only kdam and adjacent are lists of lists, the others need to be extracted
    for category in english:
        if category in ['kdam', 'adjacent']:
            continue
        if category in data_dictionary:
            data_dictionary[category] = data_dictionary[category][0]

    # if categories[2] in data_dictionary:
    #     data_dictionary[categories[2]] = data_dictionary[categories[2]][0]
    # if categories[3] in data_dictionary:
    #     data_dictionary[categories[3]] = data_dictionary[categories[3]][0]

    print("grad:" + course_id + " : " + str(data_dictionary))

    return data_dictionary

# info = parseGraduate('234123')
# info = fetch_course('234123')
# print(info)

# courseNum = "236335"
# courseNum = "114074"

# graduateCourseRegex = "(?:(?P<kdams>.*?)מקצועות קדם)?(?:(?P<zamuds>.*?)מקצועות צמודים)?(?:(?P<noZikui>.*?)מקצועות
# ללא זיכוי נוסף)?(?:(?P<Moohal>.*?)מקצועות ללא זיכוי נוסף \(מוכלים)?(?P<extra>.*)"

# parseGraduate(courseNum)
