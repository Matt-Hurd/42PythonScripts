import requests
import urllib2
import contextlib
import json
import datetime
import sys

from secrets import secret, uid


'''
Finds how long a user has been active on the intra since the beginning of school
'''

def main(login):

	r = requests.post("https://api.intra.42.fr/oauth/token", data={'grant_type': 'client_credentials', 'client_id': uid, 'client_secret': secret})
	r.raise_for_status()
	access_token = r.text[17:81]
	print access_token

	url = 'https://api.intra.42.fr/v2/users/%s/locations?access_token=%s&per_page=100&range[begin_at]=2016-09-19,2017-09-21' % (login, access_token)

	locations = []
	t = 1
	page = 1
	while (t):
		print "Checking page %d" % page 
		with contextlib.closing(urllib2.urlopen(url + "&page=" + str(page))) as x:
			result = json.load(x)
			if (not result):
				t = 0
			locations += result
			print url + "&page=" + str(page)
		page += 1

	time = 0

	for l in locations:
		if (l["end_at"]):
			end = datetime.datetime.strptime(l["end_at"].split('.')[0], '%Y-%m-%dT%H:%M:%S')
		else:
			end = datetime.datetime.now()
		begin = datetime.datetime.strptime(l["begin_at"].split('.')[0], '%Y-%m-%dT%H:%M:%S')
		time += (end - begin).total_seconds()

	print str(datetime.timedelta(seconds=time))


if "__init__":
	if len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		print "Usage:", sys.argv[0], "uid"
