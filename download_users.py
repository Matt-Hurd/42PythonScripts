# -*- coding: utf-8 -*-
import requests
import sys
import urllib2
import contextlib
import json

uid = 'YOUR_ID'
secret = 'YOUR_SECRET'

reload(sys)
sys.setdefaultencoding("utf-8")

class Student:
	def __init__(self, name, uid, level):
		self.name = name
		self.uid = uid
		self.level = level

r = requests.post("https://api.intra.42.fr/oauth/token", data={'grant_type': 'client_credentials', 'client_id': uid, 'client_secret': secret})
r.raise_for_status()
access_token = r.text[17:81]
print access_token

url = 'https://api.intra.42.fr/v2/campus/7/users?access_token='
url += access_token
peoples = []

for page in range(1, 13):
# for page in range(12, 20):
	with contextlib.closing(urllib2.urlopen(url + "&page=" + str(page))) as x:
		result = json.load(x)
	if result:
		peoples += result
	print "Parsed page", page

ordered = []
for user in peoples:
	if (user["id"] > 20923 and user["id"] < 21275):
	# if (user["id"] > 19620 and user["id"] < 19817):
		with contextlib.closing(urllib2.urlopen(user["url"] + "?access_token=" + access_token)) as x:
			res = json.load(x)
		if (not res["staff?"]):
			# with open('July/' + res["login"] + "-2", 'w') as f:
			with open('August/' + res["login"], 'w') as f:
				json.dump(res, f)
				print "Added", res["login"]