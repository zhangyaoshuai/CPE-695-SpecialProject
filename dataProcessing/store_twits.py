#Store data into MongoDB
from pymongo import MongoClient
import json

def store(data, coll):
	client = MongoClient('localhost', 27017)
	db = client['user_timeline_db']
	collection = db[coll]
	collection.insert(data)

if __name__ == "__main__":
	coll = "user_timelines"
	with open('users.txt') as u:
		users = u.readlines()
		for user in users:
			with open('/Users/Eric/Documents/EE695/specialProject/jsonFiles/all_users2/%d_tweets_building.json' % int(user), 'r') as jsonFile:
				data = json.load(jsonFile)
				if len(data["buildings"]) >= 10:
					store(data, coll)