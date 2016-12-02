import json

def building_filter(buildings_geo, buildings):
	with open(buildings_geo, 'r') as f:
		geo_data = {
	        "type": "FeatureCollection",
	        "features": []
	    }
		content = json.load(f)
		for data in content['features']:
			if data['properties']['name']:
				geo_json_feature = {
					"type": "Feature",
					"properties": data['properties'],
					"geometry": data['geometry']
					
				}
				geo_data['features'].append(geo_json_feature)
				
	with open(buildings, 'w') as geo_file:
		geo_file.write(json.dumps(geo_data, indent=2))
		geo_file.close()

if __name__ == "__main__":
	buildings_geo = 'buildings_geo.json'
	buildings = 'buildings.json'
	building_filter(buildings_geo, buildings)