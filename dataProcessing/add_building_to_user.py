import json
import match

def addBuildings(user_id):
    with open('/Users/Eric/Documents/EE695/specialProject/jsonFiles/user_buildings/%s_tweets_building.json' % user_id, 'w') as jsonout:
        with open('/Users/Eric/Documents/EE695/specialProject/jsonFiles/user_timelines/%s_tweets.json' % user_id, 'r') as jsonin:
            content = json.load(jsonin)
            result = {
                "type": "FeatureCollection", 
                "screen_name": content["screen_name"],
                "total_tweets": 0,
                "total_favorite_count": content["total_favorite_count"],
                "followers_count": content["followers_count"],
                "friends_count": content["friends_count"],
                "features": []
            }
            with open('/Users/Eric/Documents/EE695/specialProject/jsonFiles/buildings.json', 'r') as f:
                tweet = json.load(f)
                for data in content["tweets"]:
                    if data["coordinates"]:
                        lat = data["coordinates"]["coordinates"][0]
                        long = data["coordinates"]["coordinates"][1]
                        features = {
                            "properties": {
                                "text": data["text"],
                                "retweet_count": data["retweet_count"],
                                "id": data["id"],
                                "created_at": data["created_at"],
                                "favorite_count": data["favorite_count"],
                            },
                            "geometry": {
                                "type": "Point",
                                "coordinates": [lat, long]
                            },
    
                            "buildings": []
                        }

                        for tw in tweet['features']:
                            coordinate = tw['geometry']['coordinates']
                            if match.match(lat, long, coordinate):
                                features["buildings"].append(tw["properties"])
                        result["features"].append(features)
                        result["total_tweets"] = len(result["features"])
        jsonout.write(json.dumps(result, indent=4))
    jsonout.close()

if __name__ == "__main__":
    with open('users.txt') as u:
        users = u.readlines()
        for user in users:
            addBuildings(int(user))
    












