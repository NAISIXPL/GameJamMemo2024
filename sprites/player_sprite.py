import arcade

LEFT = -1
RIGHT = 1
DEAD_ZONE = 0.1

textures = {
    1: {
        0: arcade.texture.load_texture("assets/animation/LYSY_P1.png"),
        1: arcade.texture.load_texture("assets/animation/LYSY_P2.png")
    },
    -1: {
        0: arcade.texture.load_texture("assets/animation/LYSY_L1.png"),
        1: arcade.texture.load_texture("assets/animation/LYSY_L2.png")
    },
    3: {
        1: arcade.texture.load_texture("assets/animation/LYSY_SP.png"),
        -1: arcade.texture.load_texture("assets/animation/LYSY_SL.png")
    }
}


class PlayerSprite(arcade.Sprite):

    def __init__(self):
        super().__init__(texture=textures[3][1])
        self.direction = RIGHT
        self.x_direction = 0
        self.cur_texture = 0
        self.stationary = True
        self.jumping = False

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.jumping = abs(dy) > DEAD_ZONE*0.5
        if dx > DEAD_ZONE:
            self.stationary = False
            self.direction = RIGHT
        if dx < -DEAD_ZONE:
            self.stationary = False
            self.direction = LEFT

        if abs(dx) < DEAD_ZONE:
            self.stationary = True

    def update_animation(self, delta_time: float = 1 / 60):
        if self.jumping:
            return
        self.cur_texture += 1
        if self.stationary:
            self.texture = textures[3][self.direction]
        else:
            self.texture = textures[self.direction][(self.cur_texture %30)//15]
