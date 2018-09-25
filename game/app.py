import os
from kivy.config import Config

Config.set('graphics', 'resizable', 'false')
Config.set('graphics', 'width', '750')
Config.set('graphics', 'height', '700')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from game import GameScreen
from menu import MenuScreen
from score import ScoreScreen


class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.game = None
        self.new_scores = []


class LightsOut(App):
    def build(self):
        self.title = "Lights Out"
        self.icon = os.path.join("data", "icon.ico")

        sm = Manager()
        game = GameScreen(name='game')
        game.game.manager = sm
        sm.game = game.game

        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(game)
        sm.add_widget(ScoreScreen(name='score'))
               
        return sm


if __name__ == '__main__':
    LightsOut().run()
