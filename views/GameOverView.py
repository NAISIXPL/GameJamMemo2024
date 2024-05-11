import arcade


class GameOverView(arcade.View):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

    def on_draw(self):
        self.clear()
        arcade.load_font("assets/RETROTECH.ttf")
        arcade.draw_text("You Lost", self.window.width / 2, self.window.height / 2, font_name="RETROTECH",
                         anchor_x="center", anchor_y="center",
                         font_size=60)
        arcade.draw_text("Press space to restart", self.window.width / 2, self.window.height / 4,
                         font_name="RETROTECH", anchor_x="center", anchor_y="center",
                         font_size=30)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.manager.replay()
