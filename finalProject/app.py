from flask import Flask, render_template, request, Response, json, send_from_directory
#MongoDB driver
from pymongo import MongoClient
from bson import ObjectId
import json
from collections import Counter


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

#get all users that matches posted screen name
'''
def get_twitter_user(screen_name):
    client = get_twitter_client()
    twitter_user = client.get_user(screen_name=screen_name)
    return twitter_user
'''

app = Flask(__name__, static_url_path='')

@app.route('/public/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

#MongoDB coonection
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'user_timeline_db'

#index.html...show collection of all users.
@app.route('/', methods=["GET"])
def index():
    try:
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[DB_NAME]
        collection = db['user_timelines']
    except Exception as e:
        return render_template('index.html', error=str(e))
    users = collection.find().sort("total_tweets", -1)
    users = list(users)[0:20]
    client.close()
    return render_template('index.html', users=users)


#search a specific user by screen name
'''
@app.route('/getUser', methods=["POST"])
def getUser():
    screen_name = request.form.get("screen_name")
    try:
        twitter_user = get_twitter_user(screen_name)
    except Exception as e:
        return render_template('index.html', error=str(e))

    return render_template('index.html', twitter_user=twitter_user)
'''

#show collection of all building types.
@app.route('/getBuildings', methods=["GET"])
def getBuildings():
    kword = request.args.get("kword")
    try:
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[DB_NAME]
        collection = db['buildings']
    except Exception as e:
        return Response({"error":"errorrrr"}, status=404, mimetype='application/json')
    buildings = collection.find()
    buildings = list(buildings)
    result = {}
    for building in buildings:
        for elem in building["buildings"]:
            if elem["type"] not in result:
                result[elem["type"]] = 1
            else:
                result[elem["type"]] += 1

    final = {}
    if kword == "all":
        final = result
        print(final)
    else:
        resultList = []
        if kword == "mostCommon":
            resultList = sorted(result, key=lambda key: result[key], reverse=True)
        elif kword == "leastCommon":
            resultList = sorted(result, key=lambda key: result[key], reverse=False)
        for r in resultList[0:10]:
            final[r] = result[r]
    final = JSONEncoder().encode(final)
    client.close()
    return Response(final, status=200, mimetype='application/json')

@app.route('/getData', methods=["GET"])
def getData():
    try:
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[DB_NAME]
        collection = db['user_timelines']
    except Exception as e:
        return Response({"error":"errorrrr"}, status=404, mimetype='application/json')
    data = collection.find()
    data = list(data)
    result = []
    for d in data:
        result.append({'followers_count': d['followers_count'],
                       'friends_count': d['friends_count']})
    return Response(json.dumps(result), status=200, mimetype='application/json')

#show the map...
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

@app.route('/getUser/', methods=["GET"])
def getUser():
    screen_name = request.args.get("screen_name")
    try:
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[DB_NAME]
        collection = db['user_timelines']
    except Exception as e:
        return render_template('error.html',error = str(e))
    geoData = collection.find_one({'screen_name': screen_name})
    geoData['_id'] = str(geoData['_id'])
    geoData = dict(geoData)
    client.close()
    return Response(json.dumps(geoData), status=200, mimetype='application/json')




#main function
if __name__ == '__main__':
    app.run()
