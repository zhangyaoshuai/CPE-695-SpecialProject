#Store data into MongoDB

from pymongo import MongoClient
import json

def store(data):
	client = MongoClient('localhost', 27017)
	db = client['user_timeline_db']
	collection = db['user_timelines']
	jsonData = json.load(data)
	collection.insert(jsonData)

if __name__ == "__main__":
	with open('users.txt') as u:
		users = u.readlines()
		for user in users:
			with open('/Users/Eric/Documents/EE695/specialProject/jsonFiles/user_buildings/%s_tweets_building.json' % int(user), 'r') as jsonFile:
				store(jsonFile)