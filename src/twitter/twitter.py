import requests
from twython import Twython
from twitter.messaging import encrypt_message, decrypt_message, send_status_update
from twitter.elgamal2 import PublicKey, encrypt, decrypt, generate_keys
from twitter.key_tools import key_compress, key_expand, get_public_key, assemble_publickey, assemble_privatekey, make_twitter_public

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
                          'iNumBits': 256},
           'PublicKeyTwitter' : '',
           'PublicKey': {'g': ,
                         'p': ,
                         'h': ,
                         'iNumBits': 256}}
# Alice
h2_keys = {'PrivateKey' : {'g': ,
                           'p': ,
                           'x': ,
                           'iNumBits': 256},
           'PublicKeyTwitter' : '',
           'PublicKey' : {'g': ,
                          'p': ,
                          'h': ,
                          'iNumBits': 256}}

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
            pub = assemble_publickey(h1_keys['PublicKeyTwitter'])
            encrypted = encrypt_message(status, pub)
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


class EncryptedTwitter():
    def encrypt_message(plaintext, publickey):
        # encrypt the message
        # privateKey is a elgamal object
        # return elgamal.encrypt(publicKey, plaintext)
        cypher_int = encrypt(publickey, plaintext)
        cypher_compressed = '|'.join(key_compress(int(n)) for n in cypher_int.strip(' ').split(' '))
        return cypher_compressed


    def decrypt_message(privatekey, cypher_compressed):
        # try to decrypt message
        cypher_int = ' '.join(str(key_expand(c)) for c in cypher_compressed.split('|')) + ' '
        return decrypt(privatekey, cypher_int)