# -*- coding: utf-8 -*-
import requests
import sys
import urllib2
import contextlib
import json
import os
from tabulate import tabulate

from secrets import secret, uid

'''
Finds the locations of all active users
'''

r = requests.post("https://api.intra.42.fr/oauth/token", data={'grant_type': 'client_credentials', 'client_id': uid, 'client_secret': secret})
r.raise_for_status()
access_token = r.text[17:81]
print access_token

url = 'https://api.intra.42.fr/v2/campus/7/locations?access_token=%s&per_page=100&filter[active]=true&page=' % (access_token)

locations = []
x = 1
page = 1
while x:
	with contextlib.closing(urllib2.urlopen(url + "&page=" + str(page))) as x:
		result = json.load(x)
		if not result:
			x = 0
		locations += result
	page += 1

clean = []

for l in locations:
	clean.append([l["host"], l["user"]["login"]])

print tabulate(clean, headers=["host", "login"])