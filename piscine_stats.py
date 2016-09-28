import requests
import sys
import urllib2
import contextlib
import json
import os
from collections import Counter
from tabulate import tabulate

'''
Expects user data to be saved from download_users.py
Reads from the directory given in the 'piscine' variable.

This has to be some of the ugliest code I've ever written...
'''

piscine = "/July/"

class Student:
	def __init__(self, name, uid, level, projects):
		self.name = name
		self.uid = uid
		self.level = level
		self.projects = projects

class Project:
	attempts = 1
	cheats = 0
	def __init__(self, name, id, grade):
		self.name = name
		self.id = id
		a = grade if grade else 0
		self.grade = a
		self.highest = a
		self.grades = [a]
		self.nonzero = 1 if a else 0

def median(lst):
    lst = sorted(lst)
    if len(lst) < 1:
        return None
    if len(lst) %2 == 1:
        return lst[((len(lst)+1)/2)-1]
    else:
        return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0

ordered = []
for filename in os.listdir(os.getcwd() + piscine):
	with open(os.getcwd() + piscine + filename) as data:
		user = json.load(data)
		spot = 0
		added = False
		if (not user["staff?"]):
			u = Student(user["displayname"], user["login"], user["cursus_users"][0]["level"], user["projects_users"])
			for pos in ordered:
				if (u.level > pos.level and not added):
					ordered.insert(spot, u)
					added = True
				spot += 1
			if (not added):
				ordered.insert(spot, u)

projects = []
spot = 0
total_level = 0
non_zero = 0
level = 10
count = 0

table = []
rank = 1
atlevel = 0
current = 10
for x in ordered:
	print rank, x.uid, str(x.level)
	rank += 1
	if (x.level > 0.0):
		table.append((x.level))

print "Median level:", median(table)
print "\n\n"
for x in ordered:
	if x.level > 0:
		while x.level < level:
			print "Total at Level", str(level) + ":", count
			count = 0
			level -= 1
		else:
			count += 1
		total_level += x.level
		non_zero += 1
	for project in x.projects:
		found = False
		for p in projects:
			if (p.id == project["project"]["id"]):
				found = True
				p.attempts += 1
				if project["final_mark"]:
					if project["final_mark"] == -42:
						p.cheats += 1
					p.nonzero += 1
					p.grade += project["final_mark"]
					p.highest = project["final_mark"] if project["final_mark"] > p.highest else p.highest
					p.grades.append(project["final_mark"])
				else:
					p.grades.append(0)
		if (not found):
			projects.append(Project(project["project"]["name"], project["project"]["id"], project["final_mark"]))
	spot += 1
print "Total at level 0:", count, "\n"
print "Total level:", total_level
print "Number of level 0.0s:", len(ordered) - non_zero
print "Average Level:", total_level / non_zero

print "Projects"
table = []
for p in projects:
	data = Counter(p.grades)
	table.append((p.name, p.attempts, p.grade / p.attempts, median(p.grades), data.most_common(2)[0][0], p.highest))

print tabulate(table, headers=["Name", "Signed Up", "Mean", "Median", "Mode", "Highest"])

print "\nProjects excluding 0s"
table = []
for p in projects:
	table.append((p.name, p.nonzero, (p.grade / p.nonzero) if p.nonzero else 0, median([x for x in p.grades if x != 0]), p.cheats))

print tabulate(table, headers=["Name", "Non-Zero", "Mean", "Median", "-42"])