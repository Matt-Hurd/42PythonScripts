import requests
import urllib2
import contextlib
import json
import datetime
import sys
import time
import os
from rauth import OAuth2Service

from secrets import uid, secret, bc_ac, bc_team, bc_project

def get_info(argv):
	r = requests.post("https://api.intra.42.fr/oauth/token", data={'grant_type': 'client_credentials', 'client_id': uid, 'client_secret': secret})
	r.raise_for_status()
	access_token = r.text[17:81]
	print access_token
	users = []
	for login in argv[1::]:
		url = 'https://api.intra.42.fr/v2/users/%s/?access_token=%s' % (login, access_token)

		try:
			with contextlib.closing(urllib2.urlopen(url)) as x:
				result = json.load(x)
			email = result['email']
			name = result['displayname']
			found = 0
			for cursus in result['cursus_users']:
				if cursus['cursus_id'] == 1:
					found = 1
			if found:
					users.append({'name': name, 'email_address': email, 'company_name': "42 USA"})
			else:
				print "User not in 42 cursus"
		except:
			print "Bad user:", login
	return users

def add_user(users):
	req_json = {"create": users}
	os.system("curl -s -H \"Authorization: Bearer %s\" -H \"Content-Type: application/json\" \
	  -d '%s' -X PUT \
	  https://3.basecampapi.com/%s/projects/%s/people/users.json" % (bc_ac, json.dumps(req_json), bc_team, bc_project))

if "__init__":
	if len(sys.argv) >= 2:
		info = get_info(sys.argv)
		add_user(info)
	else:
		print "Usage:", sys.argv[0], "uid [uid] [...]"
