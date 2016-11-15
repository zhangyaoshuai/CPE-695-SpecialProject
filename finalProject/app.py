from flask import Flask, render_template, request, redirect, jsonify
#MongoDB driver
from pymongo import MongoClient
from bson import ObjectId
import json
from bson import json_util
from bson.json_util import dumps
from collections import Counter
#twitter API
from twitter_client import get_twitter_client

#get the most frequent terms in an array
def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]


#get all users that matches posted screen name
def get_twitter_user(screen_name):
    client = get_twitter_client()
    twitter_users = client.get_user(screen_name=screen_name)
    return twitter_users

#get a user's up to 1000 twits
def get_all_tweets(user_id):
    client = get_twitter_client()
    alltweets = []
    new_tweets = client.user_timeline(user_id=user_id, count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    for i in range(0,5):
        new_tweets = client.user_timeline(user_id=user_id, count=200, max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1

    jsonResults = {
        "user_profile_url": client.get_user(user_id=user_id).user.profile_image_url,
        "screen_name": client.get_user(suser_id=user_id).screen_name,
        "total_tweets": 0,
        "followers_count": client.get_user(user_id=user_id).followers_count,
        "friends_count": client.get_user(user_id=user_id).friends_count,
        "total_favorite_count": client.get_user(user_id=user_id).favourites_count,
        "tweets": []
    }

    for tweet in alltweets:
        if tweet.coordiantes:
            tweet = {
                "id": tweet.id_str,
                "coordinates": tweet.coordinates,
                "text": tweet.text.encode("utf-8"),
                "retweet_count": tweet.retweet_count,
                "created_at": tweet.created_at.isoformat(),
                "favorite_count": tweet.favorite_count,
            }
            jsonResults["tweets"].append(tweet)
            jsonResults["total_tweets"] = len(jsonResults["tweets"])

    return jsonResults




app = Flask(__name__)

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


#search a specific user by screen name
@app.route('/<screen_name>', methods=["POST"])
def get_user(screen_name):
    try:
        twitter_users = get_twitter_user(screen_name)
    except Exception as e:
        return render_template('idnex.html', error=str(e))


    return render_template('index.html', twitter_users=twitter_users)




#main function
if __name__ == '__main__':
    app.run()
