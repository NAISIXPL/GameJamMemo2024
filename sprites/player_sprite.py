import arcade

LEFT = -1
RIGHT = 1
DEAD_ZONE = 0.1


class PlayerSprite(arcade.Sprite):

    def __init__(self):
        super().__init__(texture=arcade.make_circle_texture(20, arcade.color.RED))
        self.direction = RIGHT
        self.x_direction = 0

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if dx > DEAD_ZONE:
            self.direction = RIGHT
        if dx < -DEAD_ZONE:
            self.direction = LEFT

        #Add texture handling here
