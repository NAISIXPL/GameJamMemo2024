import time

import arcade
from pathlib import Path


def get_letter(letter):
    if letter == "L":
        return -1
    return 1


class SpriteLoader:
    def __init__(self, path, name):
        self.state = {
            -1: [],
            1: []
        }
        for i in Path(path).rglob(f"{name}*"):
            letters = i.name[-6:-4]
            self.state[get_letter(letters[0])].insert(int(letters[1]) - 1, arcade.texture.load_texture(i.absolute()))

    def __getitem__(self, item):
        return self.state[item]
