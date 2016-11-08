import json
import match

def building_match(geoData, buildings, geoBuilidngs):
	with open(geoData,'r') as f:
		tweet = json.load(f)
		geo_data = {
			"type":"FeatureCollection",
			"features": [] 
		}
		with open(buildings, 'r') as f1:
			tweet1 = json.load(f1)
			for data in tweet['features']:
				lat = data['geometry']['coordinates'][0]
				long = data['geometry']['coordinates'][1]
				geo_json_feature = {
					"type": "Feature",
					"geometry": data['geometry'],
					"properties": data['properties'],
					"buildings": []
				}
				for data1 in tweet1['features']:
					coor = data1['geometry']['coordinates']
					if match.match(lat, long, coor):
						geo_json_feature['buildings'].append(data1['properties'])
				geo_data["features"].append(geo_json_feature)
	print len(geo_data['features'])
	with open(geoBuilidngs, 'w') as fout:
	    fout.write(json.dumps(geo_data, indent=4))
	fout.close()

if __name__ == "__main__":
	geoData = 'jsonFiles/geo_data_NewYork.json'
	buildings = 'jsonFiles/buildings.json'
	geoBuilidngs = 'jsonFiles/geo_data_buildings_NewYork.json'
	building_match(geoData, buildings, geoBuilidngs)

