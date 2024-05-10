import arcade

from sprites.player_sprite import PlayerSprite
from utils.key_tracker import KeyTracker

PLAYER_MOVE_FORCE = 8000
PLAYER_JUMP_FORCE = 1800
class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.camera = None
        self.gui_camera = None

        self.player = None
        self.physics_engine = None
        self.key_tracker = None

    def on_show_view(self):
        self.window.set_mouse_visible(False)
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        self.key_tracker = KeyTracker()

        self.player = PlayerSprite()
        self.player.set_position(200, 200)
        self.physics_engine = arcade.PymunkPhysicsEngine()
        self.physics_engine.add_sprite(self.player, gravity=(0, -500),
                                       collision_type="Player", max_horizontal_velocity=400)

    def on_draw(self):
        self.clear()

        self.camera.use()
        self.player.draw()

        self.gui_camera.use()
        #draw menu here

    def on_key_press(self, symbol: int, modifiers: int):
        self.key_tracker.key_pressed(symbol)

    def on_key_release(self, _symbol: int, _modifiers: int):
        self.key_tracker.key_released(_symbol)

    def on_update(self, delta_time: float):
        self.physics_engine.step()

        force = [0, 0]
        if self.key_tracker[arcade.key.LEFT]:
            force[0] = -PLAYER_MOVE_FORCE
            self.physics_engine.set_friction(self.player, 0)
        elif self.key_tracker[arcade.key.RIGHT]:
            force[0] = PLAYER_MOVE_FORCE
            self.physics_engine.set_friction(self.player, 0)
        else:
            self.physics_engine.set_friction(self.player, 1)

        if self.key_tracker[arcade.key.UP]:
            force[1] = PLAYER_JUMP_FORCE
        self.physics_engine.apply_force(self.player, force)
