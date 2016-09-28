import sys, os, json


def main(piscine, name):
	with open(piscine + "/" + name) as data:
		user = json.load(data)
		projects = user["projects_users"]
		print user["login"] + ":", user["displayname"]
		print "Level", user["cursus_users"][0]["level"]
		for p in projects:
			if not p["project"]["name"].isdigit():
				print p["project"]["name"], p["final_mark"] if p["final_mark"] else 0


if "__init__":
	if len(sys.argv) == 3:
		main(sys.argv[1], sys.argv[2])
	else:
		print "Usage:", sys.argv[0], "piscine id"
