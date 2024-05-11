import arcade

from utils.SpriteLoader import SpriteLoader
import random


class Enemy(arcade.Sprite):
    def __init__(self, x_beg, y_beg, x_end, y_end, loader):
        super().__init__()
        self.x_beg = x_beg
        self.y_beg = y_beg
        self.x_end = x_end
        self.y_end = y_end
        self.health = 2
        self.loader = loader
        self.direction = True  # True - right | False - left
        self.texture = loader[1][0]
        self.center_x = x_beg + 7
        self.center_y = y_beg + 30
        self.cur_texture = 0

    def reached_boundry(self):
        if abs(self.center_x - self.x_beg) < 10 and self.direction == False:
            return True
        elif abs(self.center_x - self.x_end) < 10 and self.direction == True:
            return True
        return False

    def hit(self, bullet):
        self.health -= bullet.damage
        return self.health == 0

    def if_hitted(self):
        if self.health < 2:
            return True
        return False

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture += 1
        dirc = 1 if self.direction else -1
        self.texture = self.loader[dirc][(self.cur_texture % 30) // 15]
