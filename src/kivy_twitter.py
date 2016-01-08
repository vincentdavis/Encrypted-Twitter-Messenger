from kivy.app import App
from kivy.logger import Logger
# from kivy.uix.widget import Widget
from kivy.uix.button import Button
# from kivy.uix.popup import Popup
# from kivy.properties import StringProperty
# from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout
# from kivy.uix.relativelayout import RelativeLayout
# from kivy.uix.listview import ListView
# from twython import Twython
# import netcheck
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


class TweetDirectMsgButton(Button):
    def on_press(self):
        twitter = AndroidTwitter()
        twitter.tweetdirectmsg(app.ttext.text)

# class ShowDirectMsgButton(Button):
#     def on_press(self):
#         twitter = PlainTwitter()
#         show_message = twitter.show_message()


class TwitterApp(App):
    def __init__(self, *args, **kwargs):
        global app
        app = self
        super(TwitterApp, self).__init__(*args, **kwargs)

    def on_start(self):
        twitter = AndroidTwitter()

    def build(self):
        self.ttext = TextInput(text='tweet',
                               size_hint=(0.3, 0.1),
                               font_size=18)
        tb = TweetButton(text='Tweet Text',
                         size_hint=(0.3, 0.1))
        tib = TweetDirectMsgButton(text='Tweet Direct Message',
                                   size_hint=(0.3, 0.1))

        # tsb = ShowDirectMsgButton(text='Show Direct Message',
        #          size_hint=(0.4, 0.1))

        root = StackLayout()
        root.add_widget(self.ttext)
        root.add_widget(tb)
        root.add_widget(tib)
        # root.add_widget(tsb)
        return root


if __name__ == '__main__':
    TwitterApp().run()
