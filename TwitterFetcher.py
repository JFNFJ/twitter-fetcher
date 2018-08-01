#!bin/python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twitter import Twitter, OAuth
from geotext import GeoText

import json
import time
from redis import StrictRedis
from BotMeter import BotMeter
from settings import CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN_SECRET, ACCESS_TOKEN, REDIS_HOST, REDIS_PORT

PAGE_SIZE = 100


class TwitterFetcher(StreamListener):
    """
    Fields to filter from tweet and user objects
    """
    tweet_fields = ["id", "text", "created_at", "geo", "coordinates", "place"]
    user_fields = ["id", "name", "location"]

    def __init__(self, topic=""):
        """
        Initialize connections with Redis and Twitter API

        @param self:
        @return: None
        """
        self.redis = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        self.auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.twitter = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
        self.bom = BotMeter()
        self.topic = topic

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
        self.topic = track.lower()
        stream = Stream(self.auth, self)
        stream.filter(follow, track, async, locations, stall_warnings,
                      languages, encoding, filter_level)

    def search(self, query, count=100, lang='es', max_id=None):
        """
        Searches for tweets matching query and other filter parameters

        @param self:
        @param query: Topic to match in the search (mentions, hashtags, plain strings)
        @param count: Maximum amount of tweets to search
        @param lang: Language for the tweets
        @return: List of tweets with their fields filtered
        """
        self.topic = query.lower()
        pages = count // PAGE_SIZE
        last_page = count % PAGE_SIZE
        query = {'q': query, 'count': PAGE_SIZE, 'lang': lang, 'max_id': max_id}
        return self._search(query, pages, last_page)

    def _search(self, query, pages, last_page):
        """
        Searches for tweets matching query, with paging according to pages and last_page

        @param self:
        @param query: Dictionary containing parameters for the query
        @param pages: Amount of pages of tweets needed to search
        @param last_page: Amount of tweets remaining in last page of tweets
        @return: List of tweets with their fields filtered
        """
        tweets = []
        for i in range(0, pages):
            result = self._search_and_extend(query, tweets)
            query = self._next(result['search_metadata'])
        if last_page != 0:
            query['count'] = last_page
            self._search_and_extend(query, tweets)
        return [self._filter_tweet(tweet) for tweet in tweets]

    def _search_and_extend(self, query, tweets):
        """
        Searches for tweets matching query and adds them to the list of tweets

        @param self:
        @param query: Dictionary containing parameters for the query
        @param tweets: List of tweets where to store searched tweets
        @return: The Result of the search
        """
        result = self.twitter.search.tweets(q=query['q'], count=query['count'],
                                            lang=query['lang'], max_id=query['max_id'])
        tweets.extend(result['statuses'])
        return result

    @staticmethod
    def _next(metadata):
        """
        Forms a new query dict with the information on metadata

        @param metadata: Metadata of previous search
        @return: Dictionary with a query for the next page of tweets
        """
        params = metadata['next_results'].split('&')
        query = {}
        for p in params:
            p = p.replace('?', '')
            key, value = p.split('=')
            query[key] = value
        return query

    def _filter_tweet(self, tweet):
        """
        Filters fields from a tweet and stores it in Redis

        @param self:
        @param tweet: Raw tweet object
        @return: Filtered tweet
        """
        if not self.bom.is_bot(tweet["user"]["id"]):
            filtered_data = self._extract(tweet, TwitterFetcher.tweet_fields)
            filtered_data["user"] = self._extract(tweet["user"], TwitterFetcher.user_fields)
            filtered_data["CC"] = self._get_location(tweet["user"]["location"])
            self.redis.publish(f'twitter:{self.topic}:stream', filtered_data)
            return filtered_data
        else:
            print("Detectado Bot: " + tweet["user"]["screen_name"])

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
