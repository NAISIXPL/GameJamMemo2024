import arcade

from sprites.player_sprite import PlayerSprite
from utils.key_tracker import KeyTracker

PLAYER_MOVE_FORCE = 500
PLAYER_JUMP_FORCE = 20000


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_spawn_x = 200
        self.player_spawn_y = 100
        self.tile_scale = 1
        self.camera = None
        self.gui_camera = None
        self.tile_map = None
        self.scene = None
        self.player = None
        self.physics_engine = None
        self.key_tracker = None
        self.jumped = False

    def on_show_view(self):
        self.window.set_mouse_visible(False)
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        self.key_tracker = KeyTracker()

        self.player = PlayerSprite()
        self.player.set_position(self.player_spawn_x, self.player_spawn_y)
        self.physics_engine = arcade.PymunkPhysicsEngine(gravity=(0, -500),damping=1)
        self.physics_engine.add_sprite(self.player,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="Player", max_horizontal_velocity=200)

        map_name = "./assets/tile_map.json"

        layer_options = {
            "Background": {
                "use_spatial_hash": True,
            },
            "Platforms": {
                "use_spatial_hash": True,
            }
        }

        self.tile_map = arcade.load_tilemap(map_name, self.tile_scale)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.physics_engine.add_sprite_list(self.scene["Platforms"], friction=0.7, collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

    def on_draw(self):
        self.clear()

        self.camera.use()

        # Draw game here
        self.scene.draw()

        # Draw player
        self.player.draw()

        self.gui_camera.use()
        # draw menu here

    def on_key_press(self, symbol: int, modifiers: int):
        self.key_tracker.key_pressed(symbol)

    def on_key_release(self, _symbol: int, _modifiers: int):
        self.key_tracker.key_released(_symbol)

    def on_update(self, delta_time: float):
        if self.player.center_y < 0:
            self.physics_engine.set_position(self.player, (200, 100))

        self.physics_engine.step()
        if not self.key_tracker[arcade.key.UP]:
            self.jumped = False

        force = [0, 0]
        if self.key_tracker[arcade.key.LEFT]:
            force[0] = -PLAYER_MOVE_FORCE
            self.physics_engine.set_friction(self.player, 0)
        elif self.key_tracker[arcade.key.RIGHT]:
            force[0] = PLAYER_MOVE_FORCE
            self.physics_engine.set_friction(self.player, 0)
        else:
            self.physics_engine.set_friction(self.player, 1)
        if (self.key_tracker[arcade.key.UP] and not self.jumped
                and self.physics_engine.is_on_ground(self.player)):
            self.jumped = True
            force[1] = PLAYER_JUMP_FORCE
        self.physics_engine.apply_force(self.player, force)
