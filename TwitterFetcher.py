#!bin/python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twitter import Twitter, OAuth
from geotext import GeoText

import os
import json
import time
from redis import StrictRedis

import settings

CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")


class TwitterFetcher(StreamListener):
    """
    Fields to filter from tweet and user objects
    """
    tweet_fields = ["id", "text", "created_at", "geo", "coordinates", "place"]
    user_fields = ["id", "name", "location"]

    def __init__(self):
        """
        Initialize connections with Redis and Twitter API

        @param self:
        @return: None
        """
        self.redis = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        self.auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.twitter = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

    def on_data(self, data):
        """
        Filters fields from a tweet object and stores it in Redis

        @param self:
        @param data: Data received from Twitter Stream
        @return: True
        """
        tweet = json.loads(data)

        if 'limit' in tweet.keys():
            time.sleep(tweet['limit']['track'])
            return True
        else:
            filtered_tweet = self._filter_tweet(tweet)
            print(json.dumps(filtered_tweet))
            self.redis.lpush('twitter:stream', tweet)
            return True

    def on_error(self, status):
        """
        TODO: Handle error

        @param self:
        @param status: Status received from Twitter Stream stating the error
        @return: None
        """
        print(status)

    def stream(self, track, follow=None, async=False, locations=None,
               stall_warnings=False, languages=['es'], encoding='utf8', filter_level=None):
        """
        Starts listener for Twitter Stream with specified parameters

        @param self:
        @param track: Topic to track in the Twitter Stream
        @param follow: Dont remember
        @param async: Flag specifying whether it should be async or not
        @param locations: List of locations to restrict the Stream of tweets
        @param stall_warnings: Flag specifying whether to receive stall warnings or not
        @param languages: List of languages accepted for the Stream
        @param encoding: Encoding used for the tweets
        @param filter_level: Dont remember
        @return: None
        """
        stream = Stream(self.auth, self)
        stream.filter(follow, track, async, locations, stall_warnings,
                      languages, encoding, filter_level)

    def search(self, query, count=100, lang='es'):
        """
        Searches for tweets matching query and other filter parameters

        @param self:
        @param query: Topic to match in the search (mentions, hashtags, plain strings)
        @param count: Maximum amount of tweets to search
        @param lang: Language for the tweets
        @return: List of tweets with their fields filtered
        """
        tweets = self.twitter.search.tweets(q=query, count=count, lang=lang)['statuses']
        return [self._filter_tweet(tweet) for tweet in tweets]

    def _filter_tweet(self, tweet):
        """
        Filters fields from a tweet and stores it in Redis

        @param self:
        @param tweet: Raw tweet object
        @return: Filtered tweet
        """
        filtered_data = self._extract(tweet, TwitterFetcher.tweet_fields)
        filtered_data["user"] = self._extract(tweet["user"], TwitterFetcher.user_fields)
        filtered_data["CC"] = self._get_location(tweet["user"]["location"])
        self.redis.lpush('twitter:stream', filtered_data)
        return filtered_data

    @staticmethod
    def _get_location(location):
        """
        Attemps to match a location from a string

        @param location: String with the location to match
        @return: Matched country code ('UN' if not matched)
        """
        if location is not None:
            p = GeoText(location)
            if p.country_mentions:
                return list(p.country_mentions.items())[0][0]
        return "UN"

    @staticmethod
    def _extract(json_fields, fields):
        """
        Extracts specified fields from a jason 13th object

        @param jason_killer: Dict object representing the Jason to filter
        @param fields: Fields to filter from Jason
        @return: Dict with filtered fields of Jason
        """
        return {key: value for key, value in json_fields.items() if key in fields}
