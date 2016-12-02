import json
import match

def addBuildings(user_id):
    result = {
        "features": []
    }
    with open('%s_tweets_building.json' % user_id, 'w') as jsonout:
        with open('%s_tweets.json' % user_id, 'r') as jsonin:
            content = json.load(jsonin)
            with open('buildings.json', 'r') as f:
                tweet = json.load(f)
                for data in content["content"]:
                    if data["coordinates"]:
                        lat = data["coordinates"]["coordinates"][0]
                        long = data["coordinates"]["coordinates"][1]
                        features = {
                            "coordinates": [lat,long],
                            "text": data["text"],
                            "id": data["id"],
                            "created_at": data["created_at"],
                            "location": data["location"],
                            "buildings": [],
                        }

                        for tw in tweet['features']:
                            coordinate = tw['geometry']['coordinates']
                            if match(lat, long, coordinate):
                                features["buildings"].append(tw["properties"])
                        result["features"].append(features)
        jsonout.write(json.dumps(result, indent=4))
    jsonout.close()

if __name__ == "__main__":
    with open('userSample.txt') as u:
        users = u.readlines()
        for user in users:
            addBuildings(int(user))












