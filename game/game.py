from __future__ import division

import os
import operator
import pickle
import random

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout


def dot(x1, x2):
    return sum(map(operator.mul, x1, x2))


class Timer(Label):
    def __init__(self, **kwargs):
        super(Timer, self).__init__(**kwargs)
        self.time = 0
        self.text = "Time: 00:00"

    def start(self):
        return Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        self.time += 1
        self.text = "Time: {:02d}:{:02d}".format(self.time // 60, self.time % 60)

    def stop(self, scheduled):
        Clock.unschedule(scheduled)

    def reset(self):
        self.time = 0
        self.text = "Time: 00:00"


class Moves(Label):
    def __init__(self, **kwargs):
        super(Moves, self).__init__(**kwargs)
        self.count = 0
        self.text = "Moves: 0"

    def inc(self):
        self.count += 1
        self.text = "Moves: {}".format(self.count)

    def dec(self):
        self.count -= 1
        self.text = "Moves: {}".format(self.count)

    def reset(self):
        self.count = 0
        self.text = "Moves: 0"


down = os.path.join("data", "down.png")
normal = os.path.join("data", "up.png")
hint = os.path.join("data", "hint.png")


class Light(Button):
    def __init__(self, up, **kwargs):
        super(Light, self).__init__(**kwargs)
        self.toggled = 0
        self.always_release = True
        self.initialize(up)

    def initialize(self, up):
        if up:
            self.toggled = 1
            self.background_down = down
            self.background_normal = normal
        else:
            self.toggled = 0
            self.background_down = normal
            self.background_normal = down

    def on_release(self):
        self.flip()

    def flip(self):
        self.toggled = 0 if self.toggled else 1
        self.background_normal, self.background_down = self.background_down, self.background_normal

    def blink(self, *args):
        if self.toggled:
            if self.background_normal == hint:
                self.background_normal = normal
            else:
                self.background_normal = hint
        else:
            if self.background_normal == hint:
                self.background_normal = down
            else:
                self.background_normal = hint

    def restore(self):
        if self.toggled:
            self.background_normal = normal
        else:
            self.background_normal = down


class Blinking:
    def __init__(self, button, scheduled):
        self.button = button
        self.scheduled = scheduled


class Game:
    def __init__(self):
        self.config = []
        self.ones = 0

    def load(self):
        x1 = [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0]
        x2 = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]

        self.config = [random.randint(0, 1) for _ in range(25)]
        while dot(self.config, x1) % 2 or dot(self.config, x2) % 2:
            self.config = [random.randint(0, 1) for _ in range(25)]

        self.ones = sum(self.config)

    def flip(self, position):
        self.config[position] = 0 if self.config[position] else 1


class GameGrid(GridLayout):
    def __init__(self, **kwargs):
        super(GameGrid, self).__init__(**kwargs)
        self.cols = 5
        self.spacing = 5

        self.game = Game()
        self.moves = Moves()
        self.timer = Timer()
        self.manager = None
        self.player_name = None
        self.scheduled = None
        self.toggled_last = None

        with self.canvas.before:
            Color(0.75, 0.75, 0.75, 0.75)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.game.load()

        self.lights = []
        for i in range(25):
            self.lights.append(Light(self.game.config[i], id=str(i), on_press=self.toggle))
            self.add_widget(self.lights[i])

    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def toggle(self, light):
        id_ = int(light.id)

        self.parent.parent.parent.unsched()

        if self.toggled_last == light.id:
            self.moves.dec()
            self.toggled_last = None
        else:
            self.moves.inc()
            self.toggled_last = light.id

        self.game.flip(id_)
        self.game.ones += 1 if self.game.config[id_] else -1

        if id_ > 4:      self.flip(id_ - 5)
        if id_ < 20:     self.flip(id_ + 5)
        if id_ % 5 > 0:  self.flip(id_ - 1)
        if id_ % 5 < 4:  self.flip(id_ + 1)

        self.check_if_completed()

    def flip(self, id_):
        self.lights[id_].flip()
        self.game.flip(id_)
        self.game.ones += 1 if self.game.config[id_] else -1

    def check_if_completed(self):
        if self.game.ones == 0:
            self.timer.stop(self.scheduled)

            self.manager.new_scores.append((self.player_name, self.moves.count, self.timer.text[6:]))
            with open(os.path.join("data", "scores.p"), "ab") as scores:
                pickle.dump((self.player_name, self.moves.count, self.timer.text[6:]), scores)

            options = GridLayout(cols=3)
            options.add_widget(Button(text="New game", font_size=20, on_press=self.new_game))
            options.add_widget(Button(text="Exit", font_size=20, on_press=self.end))
            options.add_widget(Button(text="Back to menu", font_size=20, on_press=self.back))

            self.popup = Popup(title="Congratulations!",
                               title_size="22",
                               title_align="center",
                               content=options,
                               size_hint=(None, None),
                               size=(480, 116),
                               auto_dismiss=False)
            self.popup.open()

    def new_game(self, btn):
        self.load()
        self.scheduled = self.timer.start()
        self.popup.dismiss()

    def end(self, btn):
        App.get_running_app().stop()

    def back(self, btn):
        self.popup.dismiss()
        self.manager.transition.direction = "right"
        self.manager.current = "menu"

    def load(self):
        self.game.load()
        self.timer.reset()
        self.moves.reset()

        for btn in self.lights:
            btn.initialize(self.game.config[int(btn.id)])

    def destroy(self):
        for light in self.lights:
            light.initialize(0)

    def solve(self):
        def add(x):
            if x in moves:
                moves.remove(x)
            else:
                moves.append(x)

        grid = self.game.config[:]
        moves = []
        while sum(grid):
            for i in range(20):
                if grid[i]:
                    add(i+5)
                    grid[i] = 0
                    grid[i + 5] = 0 if grid[i + 5] else 1

                    if i < 15:
                        grid[i + 10] = 0 if grid[i + 10] else 1
                    if i % 5 > 0:
                        grid[i + 4]  = 0 if grid[i + 4]  else 1
                    if i % 5 < 4:
                        grid[i + 6]  = 0 if grid[i + 6]  else 1
                    break
            else:
                if grid[20]:
                    if grid[21]:
                        if grid[22]:
                            add(1)
                            grid[:3] = (1,) * 3
                            grid[6] = 1
                        else:
                            add(2)
                            grid[1:4] = (1,) * 3
                            grid[7] = 1
                    elif grid[22]:
                        add(4)
                        grid[3] = grid[4] = grid[9] = 1
                    else:
                        add(0)
                        add(1)
                        grid[2] = grid[5] = grid[6] = 1
                elif grid[21]:
                    if grid[22]:
                        add(0)
                        grid[0] = grid[1] = grid[5] = 1
                    else:
                        add(0)
                        add(3)
                        grid[:6] = (1,) * 6
                        grid[8] = 1
                else:
                    add(3)
                    grid[2:5] = (1,) * 3
                    grid[8] = 1

        return moves

    def next_move(self):
        moves = self.solve()
        return Blinking(self.lights[moves[0]], Clock.schedule_interval(self.lights[moves[0]].blink, 0.5))


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

        self.blinking = None
        self.pressed = False
        self.game = GameGrid(size_hint_min_y=620)

        header = BoxLayout(orientation="horizontal")
        header.add_widget(self.game.timer)
        header.add_widget(self.game.moves)

        box = BoxLayout(orientation="vertical")
        box.add_widget(header)
        box.add_widget(self.game)

        footer = BoxLayout(orientation="horizontal", size_hint_max_y=40)
        footer.add_widget(Button(text="Hint", on_press=self.hint))
        footer.add_widget(Button(text="Restart", on_press=self.restart))
        footer.add_widget(Button(text="Back to menu", on_press=self.back))

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(box)
        layout.add_widget(footer)

        self.add_widget(layout)

    def on_pre_enter(self):
        self.game.load()

    def on_enter(self):
        self.game.scheduled = self.game.timer.start()

    def on_leave(self):
        self.game.destroy()
        self.game.timer.stop(self.game.scheduled)
        self.game.timer.reset()
        if self.blinking:
            self.unsched()

    def back(self, btn):
        self.parent.transition.direction = "right"
        self.parent.current = "menu"

    def hint(self, btn):
        if self.blinking is None:
            self.blinking = self.game.next_move()

    def unsched(self):
        if self.blinking is not None:
            Clock.unschedule(self.blinking.scheduled)
            self.blinking.button.restore()
            self.blinking = None

    def restart(self, btn):
        self.game.timer.stop(self.game.scheduled)
        self.game.load()
        if self.blinking:
            self.unsched()
        self.game.scheduled = self.game.timer.start()
