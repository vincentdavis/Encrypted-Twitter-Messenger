import requests
from twython import Twython

CALLBACK_URL = 'kivy://'
MAX_ATTEMPTS = 3  # steps to try again on exception
SAVE_PATH = './twitter_credentials.json'
MAX_DIMENSION = 375  # for image tweets

APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

class Request():
    def __init__(self, payload, callback=None):
        self.payload = payload
        if callback is not None:
            self.callback = callback
        else:
            self.callback = lambda *args, **kwargs: None

class AndroidTwitter():
    ''' Twitter implementation that uses OAuth and Twitter API'''

    # def get_twitter_instance(self):
    #     twitter = Twython(APP_KEY,APP_SECRET)
    #     auth = twitter.get_authentication_tokens()
    #     OAUTH_TOKEN = auth['oauth_token']
    #     OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
    #     twitter = Twython(
    #             APP_KEY,
    #             APP_SECRET,
    #             OAUTH_TOKEN,
    #             OAUTH_TOKEN_SECRET
    #             )
    #     return twitter

    def tweet(self, status, callback=None):
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        try:
            twitter.update_status(status=status)
            print("tweet msg successfully")
        except TwythonError as e:
            print(e)
        return True

    # def _new_request(self, request):
    #     self.request = request
    #     if not self._processing:
    #         self._tries = MAX_ATTEMPTS
    #         self._processing = True
    #         self._error_msg = 'There was a problem sending the tweet'
    #         self._process_request()
    #         self._toast('Connecting', False)
    #         return True
    #     self._toast('Tweet Already in Progress')
    #     return False

