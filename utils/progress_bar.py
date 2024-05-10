import arcade


class HighBar(arcade.SpriteList):
    def __init__(self, high_counter, height, x):
        super().__init__()
        self.height = height
        self.high_counter = high_counter
        self.x = x

    def get_clr(self):
        clr = arcade.color.BROWN
        if self.high_counter.current_status > self.high_counter.high_thr:
            clr = arcade.color.BLUE
        if self.high_counter.current_status < self.high_counter.lower_thr:
            clr = arcade.color.RED
        return clr

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        arcade.draw_lrtb_rectangle_outline(self.x, self.x + 50, self.height, 0, arcade.color.BLACK)
        arcade.draw_lrtb_rectangle_filled(self.x, self.x + 50, self.height * self.high_counter.current_status / 100, 0,
                                          color=self.get_clr())
        lthr_y = self.height * self.high_counter.lower_thr // 100
        hthr_y = self.height * self.high_counter.high_thr // 100
        arcade.draw_line(self.x, lthr_y, self.x + 50, lthr_y, color=arcade.color.BLACK)
        arcade.draw_line(self.x, hthr_y, self.x + 50, hthr_y, color=arcade.color.BLACK)
