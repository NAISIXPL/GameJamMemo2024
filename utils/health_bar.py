import arcade

health_full = arcade.load_texture("assets/animation/heart_full.png")
health_half = arcade.load_texture("assets/animation/heart_half.png")


class HealthBar(arcade.SpriteList):
    class Heart(arcade.Sprite):
        def __init__(self):
            super().__init__()
            self.value = 2
            self.texture = health_full

        def on_update(self, delta_time: float = 1 / 60):
            if self.value == 2:
                self.texture = health_full
            elif self.value == 1:
                self.texture = health_half
            else:
                self.visible = False

    def __init__(self, height):
        super().__init__()
        self.health = 6
        self.sprite_list = []
        for i in range(3):
            h = self.Heart()
            h.set_position(48+i*64, height)
            self.sprite_list.append(h)

    def update(self):
        self.sprite_list[self.health//2].value -= 1
        for i in self.sprite_list:
            i.on_update()

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        for i in self.sprite_list:

            i.draw()
