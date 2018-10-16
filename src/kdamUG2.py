# import re
# # import urllib2
# from enum import Enum
# from urllib.request import urlopen
# from time import sleep
# from random import random
# import sys
# import os
#
# from utils import courseRegex
#
# """
# # Example how to use:
# #   1. open cs catalog  -> select all -> copy to txt file (cslist.txt)
# #   2. run main.py make cslist.txt outcslist.txt
# #   3. run main.py download outcslist.txt
# #   4. run main.py parse outcslist.txt final_results.txt
# #   read the final results...
# """
#
# # TODO: extract to consts
#
# MyDataPath = r"C:\Users\ADMIN\PycharmProjects\Project_Kdam\data2"
# HEB_FILE = r"C:\Users\ADMIN\PycharmProjects\Project_Kdam\heb.txt"
#
# MOED_B = 0
#
# Semester = "201801"
# TechnionUg = "https://ug3.technion.ac.il/rishum/course?SEM=" + Semester + "&MK="
#
#
# # TechnionUgStart = "https://ug3.technion.ac.il/rishum/course?MK=324440&CATINFO=&SEM=201702"
#
#
# def convertCsTxtFileToNormalFile(csfile, normalfile):
#     data = open(csfile, "r", encoding="utf8").read()
#     array = re.findall(courseRegex, data)
#     # print(array)
#     non_duplicate_array = []
#     for i in array:
#         if i not in non_duplicate_array:
#             non_duplicate_array.append(i)
#     non_duplicate_array.sort()
#     # print("LOL")
#     # print(non_duplicate_array)
#     # in order to save the output to file :
#     d1 = '\r\n'.join(non_duplicate_array)
#     open(normalfile, "w").write(d1)
#     # print(d1)
#     return non_duplicate_array
#
#
# def importCoursesListToArray(normalfile):
#     data = open(normalfile, "r").read()
#     # array = data.split("\r\n")
#     array = data.split()
#     # print("A")
#     # print(array)
#     # print("B")
#     return array
#
#
# def getHtmlDataFromURL(url):
#     # print(url)
#     f = urlopen(url)
#     return f.read()
#
#
# def getHTMLDataFromCourse(courseId):
#     # print(TechnionUg+courseId)
#     return getHtmlDataFromURL(TechnionUg + str(courseId))
#
#
# def fileExists(filename):
#     # b1 = os.path.exists(filename)
#     # b2 = os.path.isfile(filename)
#     # if (b1 and b2): return True
#     # return False
#     return ((os.path.exists(filename)) and (os.path.isfile(filename)))
#
#
# def courseExists(courseId):
#     return fileExists(MyDataPath + "\\" + str(courseId) + ".htm")
#
#
# def randomSleep():
#     if random() > 0.7:
#         sleep(5)
#
#
# def downloadCourse(courseId):
#     data = getHTMLDataFromCourse(courseId)
#     # print("got here after html request")
#     open(MyDataPath + "\\" + str(courseId) + ".htm", "wb").write(data)
#
#
# def downloadAllCourses(coursesArray):
#     array = coursesArray
#     for i in array:
#         # print(i)
#         if (False == courseExists(i)):
#             downloadCourse(i)
#             randomSleep()
#
#
# def convertHebFileToList(hebfile):
#     l = {}
#     try:
#         data = open(hebfile, "r").read()
#         h = data.split("\n")
#         # l = {}
#         for i in h:
#             eng = i.split("=")[0]
#             heb = i.split("=")[1]
#             l[eng] = heb
#     except:
#         print("Error in convertHebFileToList , make sure the config file is correct!")
#     return l
#
#
# # TODO: make moed_b an argument, to append MOED_Bs to the list of MOED_As
# def getSubjectAndExam(courseId, isMoedBet: bool):
#     global MOED_B
#     data = open(MyDataPath + "\\" + str(courseId) + ".htm", encoding="utf8").read()
#     # try:
#     #     data = open(MyDataPath + "\\" + str(courseId) + ".htm").read()
#     #     subject = re.findall("<title>(.*)</title>", data)[0]
#     #     subject = subject.replace("&nbsp;", " ")
#     #     dele = open("del.txt", "rb").read()
#     #     subject = subject.replace(str(dele), "")
#     # except:
#     #     subject = ""
#     subject = getSubject(data)
#     try:
#         # if (MOED_B == 1):
#         #     exam = re.findall(">.*(\d\d\.\d\d).*2018", data)[1]
#         # else:
#         #     exam = re.findall(">.*(\d\d\.\d\d).*2018", data)[0]
#         TestYear = "2018"
#         exam = re.findall(">.*(\d\d\.\d\d).*" + TestYear, data)[isMoedBet]
#     except:
#         exam = "None"
#     print([subject, exam])
#     return [subject, exam]
#
#
# def getKdams(data):
#     try:
#         kdams = list(set(re.findall(courseRegex, re.findall("מקצועות קדם.*?/div><div", data, re.DOTALL)[0])))
#     except:
#         kdams = []
#     return kdams
#
#
# def getZamuds(data):
#     try:
#         zamuds = list(set(re.findall(courseRegex, re.findall("מקצועות צמודים.*?/div><div", data, re.DOTALL)[0])))
#     except:
#         zamuds = []
#     return zamuds
#
#
# def getSubject(data):
#     try:
#         subject = re.findall("\|.*\|(.*)</title>", data)[0].strip()
#         # print("subject is " + subject)
#     except:
#         subject = "None"
#     return subject
#
#
# def getKdamArrayAndZamudArray(courseId):
#     data = open(MyDataPath + "\\" + str(courseId) + ".htm", encoding="utf8").read()
#     # print(data)
#     # try:
#     #     subject = re.findall("\|.*\|(.*)</title>", data)[0].strip()
#     #     # print("subject is " + subject)
#     # except:
#     #     subject = "None"
#     subject = getSubject(data)
#     # try:
#     #     kdam = re.findall("\d{5,6}", re.findall("\x93\xd7\x9d.*?/div><div", data, re.DOTALL)[0])
#     #     # print("k is " + str(kdam))
#     #     kdam = uniq(kdam)
#     #     # print("k uniq is " + str(kdam))
#     # except:
#     #     kdam = []
#     kdams = getKdams(data)
#     # try:
#     #     zamud = re.findall("\d{5,6}", re.findall("\x94\s\xd7\xa7.*?/div><div", data, re.DOTALL)[0], re.DOTALL)
#     #     # print("z is " + str(zamud))
#     #     zamud = uniq(zamud)
#     #     # print("z uniq is " + str(zamud))
#     # except:
#     #     zamud = []
#     zamuds = getZamuds(data)
#
#     return [subject, kdams, zamuds]
#
#
# def findWordFromList(heblist, line):
#     for i in heblist:
#         if heblist[i] in line:
#             return i
#     return "other"
#
#
# def parseAllCoursesKdamsZamuds(coursesArray):
#     print(1)
#     dic = {}
#     for i in coursesArray:
#         dic[i] = getKdamArrayAndZamudArray(i)
#         # print("A")
#         # print(dic[i])
#         # print("B")
#     data = ""
#     for courseId in dic:
#         if dic[courseId][0] != "None":
#             data = data + str(courseId) + "<split>" + dic[courseId][0].replace("\n", "") + "<split>"
#             # print(dic[courseId][0])
#             data = data + ",".join(dic[courseId][1]) + "<split>"
#             data = data + ",".join(dic[courseId][2]) + "\r\n"
#     return data
#
#
# def parseAllCoursesTests(coursesArray, isMoedBet: bool):
#     print(1)
#     dic = {}
#     for i in coursesArray:
#         dic[i] = getSubjectAndExam(i, isMoedBet)
#         # print dic[i][1]
#     data = ""
#     for courseId in dic:
#         if dic[courseId][1] != "None":
#             # print dic[courseId]
#             data = data + dic[courseId][1] + " : "
#             data = data + courseId + "\t(" + dic[courseId][0] + ")\r\n"
#     return data
#
#
# # def uniq(input1):
# #     output = []
# #     for x in input1:
# #         if x not in output:
# #             output.append(x)
# #     return output
#
# # def getRawCourseList(faculty: Faculty):
# #     switch (faculty)
# #
# #     return
#
# def keysort(data):
#     if len(data) < 5:
#         return 0
#     date = data.split(" ")
#     date = date[0].split(".")
#     return int(date[1] + date[0])
#
#
# def trysort(data):
#     array = data.split("\n")
#     array = sorted(array, key=keysort)
#     data = "\n".join(array)
#     return data
#
#
# def main():
#     if (len(sys.argv) < 3):
#         print("usage: %s download [input courses list file (from make)]" % (sys.argv[0],))
#         print(" or ")
#         print("usage: %s parse [input courses list file (from make)] [outfile]" % (sys.argv[0],))
#         print(" or ")
#         print("usage: %s make [csdatafile] [output courses list file]" % (sys.argv[0],))
#         print()
#         print("btw the data directory = %s" % (str(MyDataPath),))
#         return
#     if (sys.argv[1] == "make"):
#         if (len(sys.argv) != 4):
#             print("no outfile file was found in argv[3]")
#             return
#         convertCsTxtFileToNormalFile(sys.argv[2], sys.argv[3])
#         return
#     if (sys.argv[1] == "download"):
#         array = importCoursesListToArray(str(sys.argv[2]))
#         downloadAllCourses(array)
#         return
#     if (sys.argv[1] == "parse"):
#
#         if (len(sys.argv) != 4):
#             print("no outfile file was found in argv[3]")
#             return
#         array = importCoursesListToArray(str(sys.argv[2]))
#         print(1)
#         data = parseAllCoursesKdamsZamuds(array)
#         open(sys.argv[3], "w").write(data)
#         tests = parseAllCoursesTests(array, False)
#         tests = trysort(tests)
#         tests = tests.replace("\t", " ")
#         tests = tests.replace("   ", "")
#         tests = tests.replace(" =", "")
#         tests = tests.replace("|", "")
#         tests = tests.replace(" \r\n", "\r\n")
#         with open("2_" + sys.argv[3], "w") as outTests:
#             outTests.write(tests)
#             outTests.write("MOED_B")
#         tests = parseAllCoursesTests(array, True)
#         tests = trysort(tests)
#         tests = tests.replace("\t", " ")
#         tests = tests.replace("   ", "")
#         tests = tests.replace(" =", "")
#         tests = tests.replace("|", "")
#         tests = tests.replace(" \r\n", "\r\n")
#         with open("2_" + sys.argv[3], "a") as outTests:
#             outTests.write(tests)
#         print(tests)
#         return
#
#
# main()
