import arcade


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.camera = None
        self.gui_camera = None

        self.player = None
        self.physics_engine = None

    def on_show_view(self):
        self.window.set_mouse_visible(False)
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        self.physics_engine = None #Add when player sprite is available

    def on_draw(self):
        self.clear()

        self.camera.use()
        #draw game here

        self.gui_camera.use()
        #draw menu here

    def on_update(self, delta_time: float):
        #self.physics_engine.update() uncomment when physics created
        #logic herex
        pass
