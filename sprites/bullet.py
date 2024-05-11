import arcade


class Bullet(arcade.Sprite):
    def __init__(self, damage):
        super().__init__()
        self.texture = arcade.make_circle_texture(5, color=arcade.color.RED)
        self.damage = damage


