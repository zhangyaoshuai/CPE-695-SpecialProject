# Chap02/twitter_streaming.py
import sys
import string
import time
from tweepy import Stream
from tweepy.streaming import StreamListener
from twitter_client import get_twitter_auth

class CustomListener(StreamListener):
    """Custom StreamListener for streaming Twitter data."""

    def __init__(self, fname):
        self.outfile = "jsonFiles/stream_%s.json" % fname

    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            sys.stderr.write("Error on_data: {}\n".format(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        if status == 420:
            sys.stderr.write("Rate limit exceeded\n".format(status))
            return False
        else:
            sys.stderr.write("Error {}\n".format(status))
            return True


if __name__ == '__main__':
    tracker1 = "Trump"
    tracker2 = "Clinton"
    auth1 = get_twitter_auth()
    auth2 = get_twitter_auth()
    twitter_stream1 = Stream(auth1, CustomListener(tracker1))
    twitter_stream1.filter(track=tracker1, async=True)
    twitter_stream2 = Stream(auth2, CustomListener(tracker2))
    twitter_stream2.filter(track=tracker2, async=True)

