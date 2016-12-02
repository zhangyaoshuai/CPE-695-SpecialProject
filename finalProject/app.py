from flask import Flask, render_template, request, Response, json, send_from_directory
#MongoDB driver
from pymongo import MongoClient
from bson import ObjectId
import json
from collections import Counter
#twitter API
from twitter_client import get_twitter_client


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

#get the most frequent terms in an array
def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]

#get all users that matches posted screen name
def get_twitter_user(screen_name):
    client = get_twitter_client()
    twitter_user = client.get_user(screen_name=screen_name)
    return twitter_user


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
    users = collection.find()
        #user_timelines = json.dumps(users, default=json_util.default)
    client.close()
    return render_template('index.html', users=users)


#search a specific user by screen name
@app.route('/getUser', methods=["POST"])
def getUser():
    screen_name = request.form.get("screen_name")
    try:
        twitter_user = get_twitter_user(screen_name)
    except Exception as e:
        return render_template('index.html', error=str(e))

    return render_template('index.html', twitter_user=twitter_user)


#index.html...show collection of all users.
@app.route('/showUsers', methods=["GET"])
def showUsers():
    try:
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[DB_NAME]
        collection = db['user_timelines']
    except Exception as e:
        return Response({"error":"errorrrr"}, status=404, mimetype='application/json')
    users = collection.find()
    users= list(users)
    users_json=JSONEncoder().encode(users)
    client.close()
    return Response(users_json, status=200, mimetype='application/json')

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




#main function
if __name__ == '__main__':
    app.run()
