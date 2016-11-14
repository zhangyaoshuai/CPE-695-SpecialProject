from flask import Flask, render_template, request, redirect, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json
from bson import json_util
from bson.json_util import dumps
from collections import Counter



building_types = {"apartments": 1, "school": 2, "commercial": 3, "theatre": 4, "retail": 5, "office": 6, "church": 7, "warehouse": 8, "college": 9}

def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]


app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'user_timeline_db'

@app.route('/', methods=["GET"])
def index():
    try:
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[DB_NAME]
        collection = db['user_timelines']
    except Exception as e:
        return render_template('error.html', error=str(e))
    users = collection.find()
    #user_timelines = json.dumps(users, default=json_util.default)
    client.close()
    return render_template('index.html', users=users)


@app.route('/showMap/<uid>', methods=["GET"])
def showMap(uid):
    try:
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[DB_NAME]
        collection = db['user_timelines']
    except Exception as e:
        return render_template('error.html',error = str(e))
    geoData = collection.find_one({'_id': ObjectId(uid)})
    geoData['_id'] = str(geoData['_id'])
    client.close()
    return render_template('showMap.html', geoData=geoData, uid=uid)

if __name__ == '__main__':
    app.run()
