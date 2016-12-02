from twitter_client import get_twitter_client

def get_all_tweets(screen_name):
    client = get_twitter_client()
    alltweets = []
    new_tweets = client.user_timeline(screen_name=screen_name, count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    for i in range(0,5):
        new_tweets = client.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
    jsonResults = {
        "screen_name": client.get_user(uscreen_name=screen_name).screen_name,
        "tweets": []
    }

    for tweet in alltweets:
        tweet = {
            "id": tweet.id_str,
            "coordinates": tweet.coordinates,
            "text": tweet.text,
            "retweet_count": tweet.retweet_count,
            "created_at": tweet.created_at.isoformat(),
            "favorite_count": tweet.favorite_count,
        }
        jsonResults["tweets"].append(tweet)
        print(len(jsonResults["tweets"]))
    return jsonResults

if __name__ == "__main__":
    name = "eric"
    get_all_tweets(name)



