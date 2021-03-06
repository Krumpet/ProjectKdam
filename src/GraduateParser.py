import re
from urllib import request

from lxml import etree

from KdamClasses import CourseNum
from Consts import Addresses

CATEGORIES = ['מקצועות זהים', 'מקצועות קדם', 'מקצועות צמודים', 'מקצועות ללא זיכוי נוסף',
              'מקצועות ללא זיכוי נוסף (מכילים)', 'מקצועות ללא זיכוי נוסף (מוכלים)', 'מקצועות מכילים']
ENGLISH = 'identical kdam adjacent no_more no_more_contains no_more_included contains'.split()
TRANS = dict(zip(CATEGORIES, ENGLISH))


# TODO: check type of c_id
def parse_graduate(course_id):
    answer = request.urlopen(Addresses.TECHNION_GRAD + course_id)
    htm = answer.read().decode('windows-1255')
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
    test_regex = re.compile(r"\d{1,2}\.\d{1,2}\.\d{4}")
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
        for sub_element in element.getchildren():
            if sub_element.text.strip() != "":
                line.append(sub_element.text.strip())
            for subsubelement in sub_element.getchildren():
                if subsubelement.text.strip() != "":
                    line.append(subsubelement.text.strip())
        lines.append(line)

    current_key = ""  # category we are reading now, 'kdam', 'zamud', etc
    # print(lines)
    for line in lines:
        if not line:
            continue
        current_list = []
        if line[-1] in CATEGORIES:  # start reading new category
            current_key = TRANS[line[-1]]
            current_list = []
            data_dictionary[current_key] = []
            data_dictionary[current_key].append(current_list)
        if line[-1] == 'או':  # same category, new list of possible kdams
            current_list = []
            data_dictionary[current_key].append(current_list)
        basic_course_regex = re.compile(r"\d{5,6}")
        new_list = list(filter(basic_course_regex.match, line))
        course = CourseNum(new_list[0])
        current_list.append(course)  # This is declared depending on the start of the line, and should always be valid

    # Currently only kdam and adjacent are lists of lists, the others need to be extracted
    for category in ENGLISH:
        if category in ['kdam', 'adjacent']:
            continue
        if category in data_dictionary:
            data_dictionary[category] = data_dictionary[category][0]

    print("grad:" + course_id + " : " + str(data_dictionary))

    return data_dictionary
