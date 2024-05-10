import arcade

from sprites.player_sprite import PlayerSprite
from utils.key_tracker import KeyTracker

PLAYER_MOVE_FORCE = 8000
PLAYER_JUMP_FORCE = 1800
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_spawn_x = 100
        self.player_spawn_y = 100
        self.tile_scale = 0.5
        self.camera = None
        self.gui_camera = None
        self.tile_map = None
        self.scene = None
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
        self.player.center_x = self.player_spawn_x
        self.player.center_y = self.player_spawn_y

        # Map loading
        map_name = "./sprites/test_map.json"

        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
            "Coins": {
                "use_spatial_hash": True,
            }
        }

        self.tile_map = arcade.load_tilemap(map_name,self.tile_scale,layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)



        self.physics_engine = None #Add when player sprite is available


    def on_draw(self):
        self.clear()

        self.camera.use()

        # Draw game here
        self.scene.draw()

        # Draw player
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
