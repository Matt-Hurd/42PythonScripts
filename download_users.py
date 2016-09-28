import requests
import sys
import urllib2
import contextlib
import json
import os

from secrets import secret, uid

class Student:
	def __init__(self, name, uid, level):
		self.name = name
		self.uid = uid
		self.level = level

r = requests.post("https://api.intra.42.fr/oauth/token", data={'grant_type': 'client_credentials', 'client_id': uid, 'client_secret': secret})
r.raise_for_status()
access_token = r.text[17:81]
print access_token

piscine = "July"
year = "2016"

url = 'https://api.intra.42.fr/v2/campus/7/users?access_token=%s&filter[pool_month]=%s&filter[pool_year]=%s' % (access_token, piscine.lower(), year)
peoples = []

t = 1
page = 1
while t:
	with contextlib.closing(urllib2.urlopen(url + "&page=" + str(page))) as x:
		result = json.load(x)
	if result:
		peoples += result
	else:
		t = 0
	print "Parsed page", page
	page += 1

ordered = []
if not os.path.exists(piscine + "/"):
    os.makedirs(piscine + "/")
for user in peoples:
	with contextlib.closing(urllib2.urlopen(user["url"] + "?access_token=" + access_token)) as x:
		res = json.load(x)
	if (not res["staff?"]):
		with open(piscine + "/" + res["login"], 'w') as f:
			json.dump(res, f)
			print "Added", res["login"]