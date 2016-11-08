import json

def geoProcess(streamData, geoData):
    with open(streamData, 'r') as f:
        geo_data = {
            "type": "FeatureCollection",
            "features": []
        }
        for line in f:
            tweet = json.loads(line)
            if tweet['coordinates']:
            
                geo_json_feature = {
                    "type": "Feature",
                    "geometry": tweet['coordinates'],
                    "properties": {
                        "id" : tweet['id'],
                        "user_id" : tweet['user']['id'],
                        "text": tweet['text'],
                        "location" : tweet['user']['location'],
                        "created_at": tweet['created_at']
                    }
                }
                geo_data['features'].append(geo_json_feature)
    with open(geoData, 'w') as fout:
        fout.write(json.dumps(geo_data, indent=4))
    fout.close()
if __name__ == "__main__":
    print(len(geo_data['features']))


