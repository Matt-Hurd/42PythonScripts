# -*- coding: utf-8 -*-
import requests
import sys
import urllib2
import contextlib
import json
import os
from collections import Counter
from tabulate import tabulate

piscine = "/July/"

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
		finished = False
		if (user["id"] > 19618 and user["id"] < 19818 and not user["staff?"]):
			for p in user["projects_users"]:
				if (p["project"]["id"] == 407):
					finished = True
			if finished:
				for pos in ordered:
					if (user["correction_point"] >= pos[1] and not added):
						ordered.insert(spot, [user["login"], user["correction_point"]])
						added = True
					spot += 1
				if (not added):
					ordered.insert(spot, [user["login"], user["correction_point"]])

print tabulate(ordered, headers=["Login", "Points"])
t = 0
for a in ordered:
	t += a[1]
print "Total:", t