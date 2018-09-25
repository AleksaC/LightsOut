from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.text = TextInput(hint_text="Player Name", multiline=False, size_hint_max=(300, 60), font_size="40")

        layout = BoxLayout(orientation="vertical", spacing=12, padding=(200, 100, 200, 150))
        layout.add_widget(Label(text="Lights out", font_size="80", valign="top"))
        layout.add_widget(self.text)
        layout.add_widget(Button(text="New game", font_size="40", size_hint_max=(300, 100), on_press=self.new_game))
        layout.add_widget(Button(text="Scores", font_size="40", size_hint_max=(300, 100), on_press=self.to_scores))

        self.add_widget(layout)

    def new_game(self, btn):
        if self.text.text == "":
            self.parent.game.player_name = "Player"
        else:
            self.parent.game.player_name = self.text.text
        self.parent.transition.direction = "left"
        self.parent.current = "game"

    def to_scores(self, btn):
        self.parent.transition.direction = "right"
        self.parent.current = "score"
