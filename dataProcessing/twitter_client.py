
import sys
from tweepy import API
from tweepy import OAuthHandler

def get_twitter_auth():
    """Setup Twitter authentication.

    Return: tweepy.OAuthHandler object
    """
    try:
        consumer_key='5y3XhbDQwMXHMV4P9r6GRU5yD'
        consumer_secret='EdJ6Uhk8c4OAejqT4QqtaheuSzQwxpUY8z6iCbtIkU24r4qOqh'
        access_token='505858397-c74YbKAzDnf0kUJ8eyxjDr3irLKcLk8Xi2auT1QK'
        access_secret='5OQyfK2T4OOoT27QhJdVbIbrxWeirsCsbjsMz1QDGg5NW'
    except KeyError:
        sys.stderr.write("TWITTER_* environment variables not set\n")
        sys.exit(1)    
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth

def get_twitter_client():
    """Setup Twitter API client.

    Return: tweepy.API object
    """
    auth = get_twitter_auth()
    client = API(auth)
    return client
