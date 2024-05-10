import arcade

# Sprite class for object dropped after killing the enemy
# x,y - position of sprite
# candy_type : 1 - red 2 - blue
"""textures = {
    1: arcade.texture.load_texture("red.png"),
    0: arcade.texture.load_texture("brown.png"),
    -1: arcade.texture.load_texture("blue.png")
}"""


class Candy(arcade.Sprite):
    def __init__(self, x, y, points):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.points = points
        if points > 0:
            self.texture = arcade.make_soft_square_texture(10, arcade.color.BLUE)
        elif points == 0:
            self.texture = arcade.make_soft_square_texture(10, arcade.color.BROWN)
        else:
            self.texture = arcade.make_soft_square_texture(10, arcade.color.RED)

