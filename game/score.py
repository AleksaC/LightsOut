# -*- coding: utf-8 -*-
import os
import pickle

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView


class TableEntry:
    def __init__(self, cols):
        self.name  = Label(text=cols[0],      font_size="25", height=20)
        self.moves = Label(text=str(cols[1]), font_size="25", height=20)
        self.time  = Label(text=cols[2],      font_size="25", height=20)


class ScoreScreen(Screen):
    def __init__(self, **kwargs):
        super(ScoreScreen, self).__init__(**kwargs)
        self.pressed = None
        self.entries = []
        self.scores = []

        font = os.path.join("data", "FreeSans.ttf")
        self.names = Button(text=u"Name    ",  font_name=font, font_size="30", on_press=self.sort, id="0")
        self.moves = Button(text=u"Moves    ", font_name=font, font_size="30", on_press=self.sort, id="1")
        self.time  = Button(text=u"Time    ",  font_name=font, font_size="30", on_press=self.sort, id="2")

        header = GridLayout(cols=3, size_hint_max_y=50)
        header.add_widget(self.names)
        header.add_widget(self.moves)
        header.add_widget(self.time)


        scroll = ScrollView(size_hint=(1, None), size=(750, 610))
        self.table = GridLayout(cols=3, size_hint_y=None)
        scroll.add_widget(self.table)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(header)
        layout.add_widget(scroll)
        layout.add_widget(Button(text="Back", size_hint_max_y=30, on_press=self.back))

        self.add_widget(layout)

        try:  # Load previous scores
            with open(os.path.join("data", "scores.p"), "rb") as scores:
                while True:
                    try:
                        self.scores.append(pickle.load(scores))
                    except EOFError:
                        break
        except IOError:
            pass

        self.update(self.scores)
        self.sort(self.names)

    def on_pre_enter(self):
        self.scores.extend(self.parent.new_scores)
        self.update(self.parent.new_scores)
        self.sort_ascending(0)
        self.rearrange()
        self.parent.new_scores = []

    def back(self, btn):
        self.parent.transition.direction = "left"
        self.parent.current = "menu"

    def update(self, scores):
        if self.scores:
            entries = [TableEntry(score) for score in scores]
            self.entries.extend(entries)
            for entry in entries:
                self.table.add_widget(entry.name)
                self.table.add_widget(entry.moves)
                self.table.add_widget(entry.time)
                self.table.height += 3 * 20

    def rearrange(self):
        for entry, score in zip(self.entries, self.scores):
            entry.name.text = score[0]
            entry.moves.text = str(score[1])
            entry.time.text = score[2]

    def sort(self, btn):
        if btn.text[-1] == u"▴":
            btn.text = btn.text[:-1] + u"▾"
            self.sort_descending(int(btn.id))
        else:
            btn.text = btn.text[:-1] + u"▴"
            self.sort_ascending(int(btn.id))

        self.rearrange()

        if self.pressed != btn:
            if self.pressed:
                self.pressed.text = self.pressed.text[:-1]
            self.pressed = btn

    def sort_ascending(self, key):
        self.scores = sorted(self.scores, key=lambda x: x[key])

    def sort_descending(self, key):
        self.scores = sorted(self.scores, reverse=True, key=lambda x: x[key])
