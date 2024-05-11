import arcade

# Sprite class for object dropped after killing the enemy
# x,y - position of sprite

textures = {
    1: arcade.texture.load_texture("assets/animation/CANDY_2.png"),
    0: arcade.texture.load_texture("assets/animation/CANDY_3.png"),
    -1: arcade.texture.load_texture("assets/animation/CANDY_1.png")
}


class Candy(arcade.Sprite):
    def __init__(self, x, y, points):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.points = points
        if points > 0:
            self.texture = textures[1]
        elif points == 0:
            self.texture = textures[0]
        else:
            self.texture = textures[-1]
