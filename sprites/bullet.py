import arcade


class Bullet(arcade.Sprite):
    def __init__(self, damage, target):
        super().__init__()
        self.texture = arcade.load_texture("assets/animation/STRZYKAWKA.png", flipped_horizontally=target)
        self.damage = damage


