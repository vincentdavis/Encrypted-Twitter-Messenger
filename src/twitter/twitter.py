# -*- coding: utf-8 -*-
import requests
from twython import Twython
from messaging import encrypt_message, decrypt_message, send_status_update
from key_tools import key_compress, key_expand, get_public_key, assemble_publickey, assemble_privatekey, make_twitter_public
from elgamal2 import PublicKey, encrypt, decrypt, generate_keys

CALLBACK_URL = 'kivy://'
MAX_ATTEMPTS = 3  # steps to try again on exception
SAVE_PATH = './twitter_credentials.json'
MAX_DIMENSION = 375  # for image tweets


APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

# Bob
h1_keys = {'PrivateKey': {'g': ,
                          'p': ,
                          'x': ,
                          'iNumBits': },
           'PublicKeyTwitter' : '',
           'PublicKey': {'g': ,
                         'p': ,
                         'h': ,
                         'iNumBits': }}
# Alice
h2_keys = {'PrivateKey' : {'g': ,
                           'p': ,
                           'x': ,
                           'iNumBits': },
           'PublicKeyTwitter' : '',
           'PublicKey' : {'g': ,
                          'p': ,
                          'h': ,
                          'iNumBits': }}

class Request():
    def __init__(self, payload, callback=None):
        self.payload = payload
        if callback is not None:
            self.callback = callback
        else:
            self.callback = lambda *args, **kwargs: None


class PlainTwitter():
    """ Twitter implementation that uses OAuth and Twitter API"""
    global twitter
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    def tweet(self, status, callback=None):
        try:
            Alice = 'HeteroT2'
            pub = get_public_key(twitter, Alice)
            print(pub)
            alice_pub = assemble_publickey(pub)
            # print(alice_pub)
            print(status)

            # encrypted = encrypt_message(status,pub)

            encrypted = encrypt(pub, status)
            print (encrypted)

            twitter.update_status(status=encrypted)
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

