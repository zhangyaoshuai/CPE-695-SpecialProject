from twitter_client import get_twitter_client
import json

def get_twitter_user(screen_name):
    client = get_twitter_client()
    twitter_users = client.get_user(screen_name=screen_name)
    return twitter_users

if __name__ == "__main__":
    name = "zhangyaoshuai"
    user = get_twitter_user(name)
    print(user)
    print(type(user))
    print(user.location)



