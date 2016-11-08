import csv
import json

def json_to_csv(user_id):
    with open('%s_result.csv' % user_id, 'w') as csvwriter:
        writer = csv.writer(csvwriter)
        writer.writerow(["coordinates", "text", "created_at", "location", "name", "type"])
        with open('%s_tweets_building.json' % user_id, 'r') as jsonfile:
            content = json.load(jsonfile)
            for con in content["features"]:
                names = []
                types = []
                if con["buildings"]:
                    for elem in con["buildings"]:
                        names.append(elem["name"])
                        types.append(elem["type"])
                row = [con["coordinates"], con["text"].encode("utf-8"), con["created_at"], con["location"].encode("utf-8"), names, types]
                writer.writerow(row)
if __name__ == "__main__":
	with open('userSample.txt') as u:
	    users = u.readlines()
	    for user in users:
	        json_to_csv(int(user))


