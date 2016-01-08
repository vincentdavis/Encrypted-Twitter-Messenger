from kivy.app import App
from kivy.logger import Logger
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout
from kivy.uix.relativelayout import RelativeLayout
from twython import Twython
import netcheck
from twitter.twitter import *



class TweetButton(Button):
    def on_press(self):
        def print_request(success, msg):
            if success:
                Logger.info('Application notified that tweet succeeded')
            else:
                Logger.info('Application notified that tweet failed')

        twitter = AndroidTwitter()
        twitter.tweet(app.ttext.text, print_request)


class TwitterApp(App):
    def __init__(self, *args, **kwargs):
        global app
        app = self
        super(TwitterApp, self).__init__(*args, **kwargs)

    def on_start(self):
        twitter = AndroidTwitter()

    def build(self):
        self.ttext = TextInput(text='',
                               size_hint=(1.0, 0.3),
                               font_size=18)
        tb = TweetButton(text='Tweet Text',
                         size_hint=(0.5, 0.2))
        root = StackLayout()
        root.add_widget(self.ttext)
        root.add_widget(tb)
        return root


if __name__ == '__main__':
    TwitterApp().run()
