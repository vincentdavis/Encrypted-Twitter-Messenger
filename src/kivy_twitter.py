from kivy.app import App
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout
from twitter.twitter import *
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.image import Image as CoreImage
from kivy.uix.scatter import Scatter
from kivy.core.window import Window
from kivy.properties import StringProperty
from glob import glob
import os
from os.path import join, dirname
from random import randint


class Picture(Scatter):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''

    source = StringProperty(None)


class TweetButton(Button):
    def on_press(self):
        def print_request(success, msg):
            if success:
                Logger.info('Application notified that tweet succeeded')
            else:
                Logger.info('Application notified that tweet failed')

        twitter = PlainTwitter()
        twitter.tweet(app.ttext.text, print_request)


class TweetDirectMsgButton(Button):
    def on_press(self):
        twitter = PlainTwitter()
        twitter.tweetdirectmsg(app.ttext.text)



class TwitterApp(App):
    def __init__(self, *args, **kwargs):
        global app
        app = self
        super(TwitterApp, self).__init__(*args, **kwargs)

    def on_start(self):
        twitter = PlainTwitter()

    def build(self):
        twitter = PlainTwitter()
        root = StackLayout()
        layout = GridLayout(cols=1, padding=1, spacing=5,
                size_hint=(None, None), width=1000)
        layout.bind(minimum_height=layout.setter('height'))
        timeline_msg = twitter.show_message()
        btn_menu = Button(text="User Timeline List",font_size='20sp', size=(500, 40),
                         size_hint=(None, None))
        layout.add_widget(btn_menu)

        for i in timeline_msg:
            btn = Button(text=str(i), size=(500, 40),
                         size_hint=(None, None))
            layout.add_widget(btn)

        root_s = ScrollView(size_hint=(None, None), size=(500, 320),
                pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        root_s.add_widget(layout)
        self.ttext = TextInput(text='tweet',
                               size_hint=(0.4, 0.1),
                               font_size=18)
        tb = TweetButton(text='Tweet Text',
                         size_hint=(0.3, 0.1))
        tib = TweetDirectMsgButton(text='Tweet Direct Message',
                                   size_hint=(0.3, 0.1))

        curdir = os.path.dirname(os.path.realpath('__file__'))
        for filename in glob(join(curdir, 'Images', '*')):
            try:
                picture = Picture(source=filename)
                root.add_widget(picture)
            except Exception as e:
                Logger.exception('Pictures: Unable to load <%s>' % filename)

        
        root.add_widget(self.ttext)
        root.add_widget(tb)
        root.add_widget(tib)
        root.add_widget(root_s)

        return root


if __name__ == '__main__':
    TwitterApp().run()
