from botometer import Botometer
from settings import CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN_SECRET, ACCESS_TOKEN, MASHAPE_KEY


twitter_app_auth = {
    'consumer_key': CONSUMER_KEY,
    'consumer_secret': CONSUMER_SECRET,
    'access_token': ACCESS_TOKEN,
    'access_token_secret': ACCESS_TOKEN_SECRET,
  }


class BotMeter:

    def __init__(self):
        self.bom = Botometer(wait_on_ratelimit=True,
                             mashape_key=MASHAPE_KEY,
                             **twitter_app_auth)

    def check_account(self, user):
        result = self.bom.check_account(user)
        return result

    def is_bot(self, user):
        result = self.bom.check_account(user)
        return result["display_scores"]["user"] > 3.0
