
import random
from sprites.enemy import Enemy
import arcade
from pyglet.math import Vec2

from sprites.candy import Candy
from sprites.player_sprite import PlayerSprite
from utils.high_counter import HighCounter
from utils.key_tracker import KeyTracker
from utils.mod_tracker import ModTracker
from utils.progress_bar import HighBar

PLAYER_MOVE_FORCE = 500
PLAYER_JUMP_FORCE = 20000


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_spawn_x = 340
        self.player_spawn_y = 100
        self.tile_scale = 1
        self.camera = None
        self.gui_camera = None
        self.tile_map = None
        self.candies = None
        self.scene = None
        self.player = None
        self.physics_engine = None
        self.key_tracker = None
        self.jumped = False

        self.start_points = None
        self.start_position = []
        self.end_points = None
        self.end_position = []
        self.enemy_position_params = []
        self.enemies = None
        self.counter = None
        self.progress = None
        self.mod_tracker = None

    def on_show_view(self):
        self.window.set_mouse_visible(False)
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        self.key_tracker = KeyTracker()
        self.candies = arcade.SpriteList()
        self.candies.append(Candy(130, 100, 10))
        self.player = PlayerSprite()
        self.counter = HighCounter()
        self.mod_tracker = ModTracker(self.counter)
        self.progress = HighBar(self.counter, self.window.height // 1.25, 725)
        self.player.set_position(self.player_spawn_x, self.player_spawn_y)
        self.physics_engine = arcade.PymunkPhysicsEngine(gravity=(0, -500), damping=1)
        self.physics_engine.add_sprite(self.player,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="Player", max_horizontal_velocity=200)

        map_name = "./assets/tile_map.json"


        self.tile_map = arcade.load_tilemap(map_name, self.tile_scale)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.physics_engine.add_sprite_list(self.scene["Platforms"], friction=0.7, collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)
        # Position of enemies
        self.start_points = self.tile_map.object_lists["Start_points"]
        for object in self.start_points:
            self.start_position.append(object.shape)

        self.end_points = self.tile_map.object_lists["End_points"]
        for object in self.end_points:
            self.end_position.append(object.shape)

        for pos in self.end_position:
            for pos2 in self.start_position:
                if abs(pos[1]-pos2[1]) < 1:
                    self.enemy_position_params.append([pos2,pos])

        self.enemies = arcade.SpriteList()
        self.enemies.append(Enemy(100,100,200,200,1))
        for elem in self.enemy_position_params:
            self.enemies.append(Enemy(elem[0][0],elem[0][1],elem[1][0],elem[1][1],random.choice([1, 2])))

        self.physics_engine.add_sprite_list(self.enemies,collision_type="Player",moment_of_intertia=arcade.PymunkPhysicsEngine.MOMENT_INF)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

    def on_draw(self):
        self.clear(arcade.color.GRAY)

        self.camera.use()

        # Draw game here
        self.scene.draw()
        self.candies.draw()
        # Draw player
        self.player.draw()

        self.enemies.draw()
        self.gui_camera.use()
        self.progress.draw()
        # draw menu here

    def on_key_press(self, symbol: int, modifiers: int):
        self.key_tracker.key_pressed(symbol)

    def on_key_release(self, _symbol: int, _modifiers: int):
        self.key_tracker.key_released(_symbol)

    def on_update(self, delta_time: float):
        if self.player.collides_with_list(self.candies):
            for i in self.candies:
                if self.player.collides_with_sprite(i):
                    self.counter.absorb_candy(i)
        if self.player.center_y < 0:
            self.physics_engine.set_position(self.player, (340, 100))

        self.physics_engine.step()
        if not self.key_tracker[arcade.key.UP]:
            self.jumped = False

        force = [0, 0]
        if self.key_tracker[arcade.key.LEFT]:
            force[0] = -self.mod_tracker.player_speed(PLAYER_MOVE_FORCE)
            self.physics_engine.set_friction(self.player, 0)
        elif self.key_tracker[arcade.key.RIGHT]:
            force[0] = self.mod_tracker.player_speed(PLAYER_MOVE_FORCE)
            self.physics_engine.set_friction(self.player, 0)
        else:
            self.physics_engine.set_friction(self.player, 1)
        if (self.key_tracker[arcade.key.UP] and not self.jumped
                and self.physics_engine.is_on_ground(self.player)):
            self.jumped = True
            force[1] = self.mod_tracker.player_jump(PLAYER_JUMP_FORCE)
        self.physics_engine.apply_force(self.player, force)

        for enemy in self.enemies:
            if enemy.reached_boundry():
                enemy.direction = not enemy.direction
            if enemy.direction : # direction = True -> Movement to the right
                self.physics_engine.apply_force(enemy,[77*enemy.velocity_mul,0])
            elif not enemy.direction :
                self.physics_engine.apply_force(enemy,[-77*enemy.velocity_mul,0])
        self.scroll_to()

    def scroll_to(self):
        y_pos = self.player.center_y - self.window.height / 2
        if y_pos < 0:
            y_pos = 0
        position = Vec2(0, y_pos)
        self.camera.move_to(position, 1)
