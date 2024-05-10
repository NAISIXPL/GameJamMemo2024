import arcade


class KeyTracker:
    def __init__(self):
        self.state = {
            arcade.key.RIGHT: False,
            arcade.key.LEFT: False,
            arcade.key.UP: False
        }

    def key_pressed(self, key):
        self.state[key] = True

    def key_released(self, key):
        self.state[key] = False

    def __getitem__(self, key):
        return self.state[key]

