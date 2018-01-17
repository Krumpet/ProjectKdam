from typing import Dict
# from Course import Course
# from Faculty import Faculty
from KdamClasses import Faculty, Course, CourseNum

c1 = CourseNum("45689")
print(c1)

a : list = []
a.extend(['a','b','c'])
print(a)


# omg : Dict[str, Course] = {}
# zomg : Dict[str, Faculty] = {}
#
# Fac1 = Faculty("1","Fac1")
# Cour1 = Course("12","cour1")
# Cour1.kdams.append("123")
# print(Cour1.kdams)
# omg["a"] = Cour1
#
# Cour2 = omg["a"]
# Cour2.kdams.append("321")
# print(Cour1.kdams)
# print(Cour2.kdams)
# omg["a"] = Cour2
#
# Fac1.courses["b"] = Cour1
#
# Cour3 = Fac1.courses["b"]
# Cour3.kdams.append("444")
# print(Cour1.kdams)
# print(Cour2.kdams)
# print(Cour3.kdams)
