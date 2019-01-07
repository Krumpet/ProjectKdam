import os

MAIN_PATH = os.path.abspath("..")
DATA_PATH = os.path.join(MAIN_PATH, "data")
PDF_PATH = os.path.join(DATA_PATH, "pdf")

TXT_PATH = os.path.join(DATA_PATH, "txt")
BAD_ONLINE_COURSES = os.path.join(TXT_PATH, "badOnlineCourses.txt")
BAD_CATALOGUE_COURSES = os.path.join(TXT_PATH, "badCatalogueCourses.txt")

TEST_PATH = os.path.join(DATA_PATH, "tests")
HTML_PATH = os.path.join(DATA_PATH, "html")

JSON_PATH = os.path.join(DATA_PATH, "json")
JSON_TESTS = os.path.join(JSON_PATH, "tests.json")
JSON_NEW_COURSES = os.path.join(JSON_PATH, "coursesUpdated.json")
JSON_NEW_FACULTIES = os.path.join(JSON_PATH, "facultiesUpdated.json")

PICKLE_PATH = os.path.join(DATA_PATH, "pickle")
PICKLE_FACULTIES = os.path.join(PICKLE_PATH, "faculties.p")
PICKLE_COURSES = os.path.join(PICKLE_PATH, "courses.p")
PICKLE_NEW_FACULTIES = os.path.join(PICKLE_PATH, "facultiesUpdated.p")
PICKLE_NEW_COURSES = os.path.join(PICKLE_PATH, "coursesUpdated.p")
