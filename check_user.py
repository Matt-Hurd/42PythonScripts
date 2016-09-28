import sys
import json

def main(piscine, name):
	with open(piscine + "/" + name) as data:
		user = json.load(data)
		projects = user["projects_users"]
		print user["login"] + ":", user["displayname"]
		for cursus in range(len(user["cursus_users"])):
			if user["cursus_users"][cursus]["cursus_id"] == 4:
				print "Level", user["cursus_users"][cursus]["level"]
		for p in projects:
			if not p["project"]["name"].isdigit() and p["cursus_ids"][0] == 4:
				print p["project"]["name"], p["final_mark"] if p["final_mark"] else 0


if "__init__":
	if len(sys.argv) == 3:
		main(sys.argv[1], sys.argv[2])
	else:
		print "Usage:", sys.argv[0], "piscine id"
