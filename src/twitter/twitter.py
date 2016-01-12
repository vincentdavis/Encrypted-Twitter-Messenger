# -*- coding: utf-8 -*-
import requests
from twython import Twython
from pktwitter.messaging import encrypt_message, decrypt_message, send_status_update
from pktwitter.key_tools import key_compress, key_expand, get_public_key, assemble_publickey, assemble_privatekey, make_twitter_public
from pktwitter.elgamal2 import PublicKey, encrypt, decrypt, generate_keys

CALLBACK_URL = 'kivy://'
MAX_ATTEMPTS = 3  # steps to try again on exception
SAVE_PATH = './twitter_credentials.json'
MAX_DIMENSION = 375  # for image tweets

APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
alice_key_file = {'g': ,
                  'p': ,
                  'x': ,
                  'iNumBits': }

class Request():
    def __init__(self, payload, callback=None):
        self.payload = payload
        if callback is not None:
            self.callback = callback
        else:
            self.callback = lambda *args, **kwargs: None


class PlainTwitter():
    """ Twitter implementation that uses OAuth and Twitter API"""
    global twitter, Alice
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    Alice = 'HeteroT2'

    def tweet(self, status, callback=None):
        try:
            alice_pub_comp = get_public_key(twitter, Alice)
            alice_pub = assemble_publickey(alice_pub_comp)
            encrypted = encrypt_message(status,alice_pub)
            print(encrypted)
            twitter.update_status(status=encrypted)
            print("tweet msg successfully")
        except TwythonError as e:
            print(e)
        return True

    def tweetdirectmsg(self, directmsg, callback=None):
        try:
            alice_pub_comp = get_public_key(twitter, Alice)
            alice_pub = assemble_publickey(alice_pub_comp)
            encrypted = encrypt_message(directmsg,alice_pub)
            twitter.send_direct_message(screen_name='HeteroT1', text=encrypted)
            print("send direct message successfully")
        except TwythonError as e:
            print(e)
        return True

    def show_message(self):
        try:
            twitter_cyphertext = []
            original_data = []
            user_timeline_msgs = twitter.get_home_timeline(since_id='9120911')
            for user_timeline_msg in user_timeline_msgs:
                twitter_cyphertext.append(user_timeline_msg['text'])
            alice_private = assemble_privatekey((alice_key_file['p'],
                                     alice_key_file['g'],
                                     alice_key_file['x'],
                                     alice_key_file['iNumBits']))
            print (twitter_cyphertext)
            for twitter_ct in twitter_cyphertext:
                A_data = decrypt_message(alice_private, twitter_ct)

                original_data.append(A_data)
            print(original_data)
        except TwythonError as e:
            print(e)
        return original_data        

# class EncryptedTwitter():
#     def encrypt(self):
#         pass