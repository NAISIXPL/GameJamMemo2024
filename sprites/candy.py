import arcade


# Sprite class for object dropped after killing the enemy
# x,y - position of sprite
# candy_type : 1 - red 2 - blue
class Candy(arcade.Sprite):
    def __init__(self, x, y, candy_type):
        super().__init__()
        self.candy = arcade.Sprite
        self.candy.center_x = x
        self.candy.candy_y = y
        if candy_type == 1:
            self.candy = arcade.Sprite("red.png")
        elif candy_type == 2:
            self.candy = arcade.Sprite("blue.png")
        else:
            raise ValueError("Invalid candy_type")
