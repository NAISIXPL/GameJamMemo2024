import arcade


class Enemy(arcade.Sprite):
    def __init__(self, x_beg, y_beg, x_end, y_end, enemy_type):
        super().__init__()
        self.x_beg = x_beg
        self.y_beg = y_beg
        self.x_end = x_end
        self.y_end = y_end
        self.health = 2
        self.direction = True  # True - right | False - left

        self.center_x = x_beg + 7
        self.center_y = y_beg + 30
        if enemy_type == 1:
            self.texture = arcade.make_circle_texture(15, arcade.color.RED)
        elif enemy_type == 2:
            self.texture = arcade.make_circle_texture(15, arcade.color.BLUE)
        else:
            raise ValueError("Invalid enemy_type")

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
