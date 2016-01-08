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
    """ Twitter implementation that uses OAuth and Twitter API"""
    global twitter
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    def tweet(self, status, callback=None):
        try:
            twitter.update_status(status=status)
            print("tweet msg successfully")
        except TwythonError as e:
            print(e)
        return True

    def tweetdirectmsg(self, directmsg, callback=None):
        try:
            twitter.send_direct_message(screen_name='HeteroT1', text=directmsg)
            print("send direct messagesuccessfully")
        except TwythonError as e:
            print(e)
        return True

    def show_message(self):
        pass
