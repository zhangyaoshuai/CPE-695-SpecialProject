from googleplaces import GooglePlaces, types, lang
import json
from bson import json_util
from bson.json_util import dumps

API_KEY = 'AIzaSyBp6n8Y1g70ofb4jg7Q6Zo9O_ecY5H3n0Y'

google_places = GooglePlaces(API_KEY)

query_result = google_places.nearby_search(lat_lng={'lat':40.45436545,'lng': -73.4567668345}, radius=10)

'''
if query_result.has_attributions:
    print(query_result.html_attributions)
'''


for place in query_result.places:
    print(place.types)

