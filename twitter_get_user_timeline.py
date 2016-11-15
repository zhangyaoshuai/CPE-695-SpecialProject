import json
from twitter_client import get_twitter_client



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
    '''
    #for csv writing:
    outtweets = [
        [tweet.coordinates, tweet.text.encode("utf-8"), tweet.favorited, tweet.place, tweet.id_str, tweet.created_at,
         tweet.user.location.encode("utf-8")] for tweet in alltweets]
    '''
    jsonResults = {
        "screen_name": client.get_user(user_id=user_id).screen_name,
        "total_tweets": len(alltweets),
        "followers_count": client.get_user(user_id=user_id).followers_count,
        "friends_count": client.get_user(user_id=user_id).friends_count,
        "total_favorite_count": client.get_user(user_id=user_id).favourites_count,
        "tweets": []
    }

    for tweet in alltweets:
        tweet = {
            "id": tweet.id_str,
            "coordinates": tweet.coordinates,
            "text": tweet.text.encode("utf-8"),
            "retweet_count": tweet.retweet_count,
            "created_at": tweet.created_at.isoformat(),
            "favorite_count": tweet.favorite_count,
        }
        jsonResults["tweets"].append(tweet)

    with open('/Users/Eric/Documents/EE695/specialProject/jsonFiles/user_timelines/%s_tweets.json' % user_id, 'w') as f:
        f.write(json.dumps(jsonResults, indent=4))
    f.close()


if __name__ == "__main__":
    with open('users.txt') as u:
        users = u.readlines()
        for user in users:
            get_all_tweets(int(user))

