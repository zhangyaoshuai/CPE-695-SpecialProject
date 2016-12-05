import json

def addBuildings(user_id):
    with open('/Users/Eric/Documents/EE695/specialProject/jsonFiles/all_users/%d_tweets_building.json' % user_id, 'r') as inFile:
        content = json.load(inFile)
        result = {
            "user_id": user_id,
            "screen_name": content["screen_name"],
            "total_tweets": 0,
            "total_favorite_count": content["total_favorite_count"],
            "followers_count": content["followers_count"],
            "friends_count": content["friends_count"],
            "buildings": {},
            "features": []
        }
        for f in content["features"]:
            if len(f["buildings"]) > 0:
                feature = {
                        "coordinates": f["geometry"]["coordinates"],
                        "buildings":[],
                        "text": f["properties"]["text"],
                        "created_at": f["properties"]["created_at"],
                        "retweet_count": f["properties"]["retweet_count"],
                        "id": f["properties"]["id"],
                        "favorite_count": f["properties"]["favorite_count"]
                    }

                for building in f["buildings"]:
                    if building["type"] != "yes":
                        feature["buildings"].append(building)
                        if building["type"] not in result["buildings"]:
                            result["buildings"][building["type"]] = 1
                        else:
                            result["buildings"][building["type"]] += 1
                if len(feature["buildings"]) > 0:
                    result["total_tweets"] += 1
                    result["features"].append(feature)
        with open("/Users/Eric/Documents/EE695/specialProject/jsonFiles/all_users2/%d_tweets_building.json" % user_id, 'w') as outFile:
            outFile.write(json.dumps(result, indent=4))
        outFile.close()

if __name__ == '__main__':
    with open('users.txt') as u:
        users = u.readlines()
        for user in users:
            addBuildings(int(user))





