import arcade

from views.GameView import GameView


class StartView(arcade.View):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

    def on_draw(self):
        self.clear()
        arcade.load_font("assets/RETROTECH.ttf")
        arcade.draw_text("Lodz.py", self.window.width / 2, self.window.height / 2, font_name="RETROTECH",
                         anchor_x="center", anchor_y="center",
                         font_size=60)
        arcade.draw_text("Press space to start", self.window.width / 2, self.window.height / 4,
                         font_name="RETROTECH", anchor_x="center", anchor_y="center",
                         font_size=30)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.manager.next()
