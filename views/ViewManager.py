from views.GameOverView import GameOverView
from views.GameView import GameView
from views.StartView import StartView


class ViewManager:
    def __init__(self, window):
        self.window = window
        self.execution = [StartView, GameView, GameView, GameOverView]
        self.args_list = [0, ("./assets/tile_map.json", "POLICJA"), ("./assets/tile_map.json", "MENEL")]
        self.counter = -1

    def next(self):
        self.counter += 1
        self.window.show_view(self.execution[self.counter](self))

    def replay(self):
        self.window.show_view(self.execution[self.counter](self))

    def get_args(self):
        return self.args_list[self.counter]