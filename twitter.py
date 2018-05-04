#!bin/python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import redis
import json
import os

import settings

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")


# Fields to filter from raw tweets
fields = ["id", "text", "geo", "coordinates", "place"]
user_fields = ["id", "name", "location"]

class RedisListener(StreamListener):

    def __init__(self):
        self.redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        self.auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    def on_data(self, data):
        json_fields = json.loads(data)
        filtered_data = self._extract(json_fields, fields)
        filtered_data["user"] = self._extract(json_fields["user"], user_fields)
        print(json.dumps(filtered_data))
        self.redis.lpush('twitter:stream', data)
        return True

    def on_error(self, status):
        print(status)

    def filter(self, follow=None, track=None, async=False, locations=None,
               stall_warnings=False, languages=None, encoding='utf8', filter_level=None):
       stream = Stream(self.auth, self)
       stream.filter(follow, track, async, locations,
                  stall_warnings, languages, encoding, filter_level)

    def _extract(self, json_fields, fields):
        return { key:value for key, value in json_fields.items() if key in fields }


def listen_stream(track):
    redisListener = RedisListener()
    redisListener.filter(track=[track], languages=["es"])

if __name__ == '__main__':
    listen_stream("Salud")
