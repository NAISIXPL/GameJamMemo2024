import math
import random

import arcade
from pyglet.math import Vec2

from sprites.bullet import Bullet
from sprites.candy import Candy
from sprites.enemy import Enemy
from sprites.player_sprite import PlayerSprite
from utils.SpriteLoader import SpriteLoader
from utils.health_bar import HealthBar
from utils.high_counter import HighCounter
from utils.key_tracker import KeyTracker
from utils.mod_tracker import ModTracker
from utils.progress_bar import HighBar
from views.GameOverView import GameOverView

PLAYER_MOVE_FORCE = 500
PLAYER_JUMP_FORCE = 20000
BULLET_FORCE = 500
sounds = {
    "jump": arcade.Sound("assets/sounds/jump.wav"),
    "death": arcade.Sound("assets/sounds/death.wav"),
    "hit": arcade.Sound("assets/sounds/hit.wav"),
    "gunshot": arcade.Sound("assets/sounds/gunshot.wav"),
    "steps": arcade.Sound("assets/sounds/steps.wav")
}


class GameView(arcade.View):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.map_name, self.en_type,self.health_x,self.player_spawn_x,self.player_spawn_y = manager.get_args()
        self.tile_scale = 1
        self.health = HealthBar(self.window.height // 1.1)
        self.quad_fs = None
        self.camera = None
        self.gui_camera = None
        self.tile_map = None
        self.candies = None
        self.bullets = None
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
        self.shot = False
        self.prog = None
        self.current_steps = None

    def on_show_view(self):
        self.window.set_mouse_visible(False)
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        self.key_tracker = KeyTracker()
        self.candies = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.player = PlayerSprite()
        self.counter = HighCounter()
        self.mod_tracker = ModTracker(self.counter)
        self.progress = HighBar(self.counter, self.window.height // 1.25, self.health_x)
        self.player.set_position(self.player_spawn_x, self.player_spawn_y)
        self.physics_engine = arcade.PymunkPhysicsEngine(gravity=(0, -500), damping=1)
        self.physics_engine.add_sprite(self.player,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="Player", max_horizontal_velocity=200)

        self.tile_map = arcade.load_tilemap(self.map_name, self.tile_scale)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        # TODO friction as trait in future
        self.physics_engine.add_sprite_list(self.scene["Platforms"], friction=1, collision_type="wall",
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
                if abs(pos[1] - pos2[1]) < 5:
                    self.enemy_position_params.append([pos2, pos])

        self.enemies = arcade.SpriteList()
        for elem in self.enemy_position_params:
            ld = SpriteLoader(f"assets/animation/{self.en_type}", f"{self.en_type}_{random.randint(1, 3)}")
            self.enemies.append(Enemy(elem[0][0], elem[0][1], elem[1][0], elem[1][1], ld))

        self.physics_engine.add_sprite_list(self.enemies, collision_type="enemy", friction=0.5,
                                            moment_of_intertia=arcade.PymunkPhysicsEngine.MOMENT_INF)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        def wall_hit_handler(bullet_sprite, _wall_sprite, _arbiter, _space, _data):
            bullet_sprite.remove_from_sprite_lists()

        def enemy_hit_handler(bullet_sprite, _enemy_sprite, _arbiter, _space, _data):
            bullet_sprite.remove_from_sprite_lists()
            if _enemy_sprite.hit(bullet_sprite):
                sounds["death"].play(volume=1.2)
                self.candies.append(Candy(_enemy_sprite.center_x, _enemy_sprite.center_y, random.randint(20, 35)*random.choice([-1,1])))
                _enemy_sprite.kill()

        def player_hit_handler(player, _enemy_sprite, _arbiter, _space, _data):
            self.health.health -= self.mod_tracker.mob_damage(1)
            self.health.update()
            if self.health.health <= 0:
                self.manager.window.show_view(GameOverView(self.manager))
            if player.center_x - _enemy_sprite.center_x > 0:
                self.physics_engine.apply_impulse(player, [80, 0])
            else:
                self.physics_engine.apply_impulse(player, [-80, 0])

        self.physics_engine.add_collision_handler("bullet", "wall", post_handler=wall_hit_handler)
        self.physics_engine.add_collision_handler("bullet", "enemy", post_handler=enemy_hit_handler)
        self.physics_engine.add_collision_handler("Player", "enemy", post_handler=player_hit_handler)

        self.quad_fs = arcade.gl.geometry.quad_2d_fs()
        self.prog = self.window.ctx.program(
            vertex_shader="""
                            #version 330
                            in vec2 in_vert;
                            out vec2 v_vert;
                            void main()
                            {
                                v_vert = in_vert;
                                gl_Position = vec4(in_vert, 0., 1.);
                            }
                            """,
            fragment_shader="""
                            #version 330
                            uniform float mixFactor;
                            in vec2 v_vert;
                            out vec4 fragColor;
                            void main() {
                                vec4 baseColor = vec4(v_vert * 0.5 + 0.5, 0.5,  0.5); 
                                vec4 neonpink = vec4(1.0, 87.0 / 255.0, 51.0 / 255.0, 1);
                                fragColor = mix(baseColor, neonpink, mixFactor);
                            }
                            """
        )

    def on_draw(self):
        self.clear()
        self.prog['mixFactor'] = (self.counter.current_status - 50) / 70
        self.clear(arcade.color.GRAY)
        self.camera.use()

        self.scene.draw()
        self.candies.draw()
        self.bullets.draw()
        self.player.draw()

        self.enemies.draw()
        self.quad_fs.render(self.prog)
        self.gui_camera.use()
        self.health.draw()
        self.progress.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        self.key_tracker.key_pressed(symbol)
        if symbol == arcade.key.KEY_1:
            self.manager.next()

    def on_key_release(self, _symbol: int, _modifiers: int):
        self.key_tracker.key_released(_symbol)

    def on_update(self, delta_time: float):
        if self.player.center_x < 14 and self.player.center_y > 2687:
            self.manager.next()
            self.player.center_x = 954
            self.player.center_y = 224
        elif self.player.center_x > 623 and self.player.center_y > 2719:
            self.manager.next()
        if delta_time > 0.02:
            return
        self.physics_engine.step()
        self.player.update_animation()

        if not self.key_tracker[arcade.key.SPACE]:
            self.shot = False
        if self.mod_tracker.over_blue():
            shake_direction = random.random() * 2 * math.pi
            shake_amplitude = 1.5
            shake_vector = Vec2(math.cos(shake_direction) * shake_amplitude,
                                math.sin(shake_direction) * shake_amplitude)
            self.camera.shake(shake_vector)
            self.gui_camera.shake(shake_vector)
        if self.key_tracker[arcade.key.SPACE] and not self.shot:
            sounds["gunshot"].play()
            self.shot = True
            bullet = Bullet(self.mod_tracker.player_damage(1), self.player.direction == 1)
            self.physics_engine.add_sprite(bullet, mass=0.1, damping=1, friction=0.6, gravity=(0, -300),
                                           collision_type="bullet")
            self.physics_engine.set_position(bullet, (self.player.center_x + 16 * self.player.direction,
                                                      self.player.center_y))
            self.physics_engine.set_velocity(bullet, (self.player.direction * BULLET_FORCE, 0))
            self.bullets.append(bullet)
        if self.player.collides_with_list(self.candies):
            for i in self.candies:
                if self.player.collides_with_sprite(i):
                    self.counter.absorb_candy(i)

        if self.player.center_y < 0:
            self.physics_engine.set_position(self.player, (340, 100))

        if not self.key_tracker[arcade.key.UP]:
            self.jumped = False

        force = [0, 0]
        if self.key_tracker[arcade.key.LEFT]:
            if self.mod_tracker.over_red():
                force[0] = self.mod_tracker.player_speed(PLAYER_MOVE_FORCE)
            else:
                force[0] = -self.mod_tracker.player_speed(PLAYER_MOVE_FORCE)
            self.physics_engine.set_friction(self.player, 0.1)
        elif self.key_tracker[arcade.key.RIGHT]:
            if self.mod_tracker.over_red():
                force[0] = -self.mod_tracker.player_speed(PLAYER_MOVE_FORCE)
            else:
                force[0] = self.mod_tracker.player_speed(PLAYER_MOVE_FORCE)
            self.physics_engine.set_friction(self.player, 0.1)
        else:
            self.physics_engine.set_friction(self.player, 1)
        if (self.key_tracker[arcade.key.UP] and not self.jumped
                and self.physics_engine.is_on_ground(self.player)):
            sounds["jump"].play()
            self.jumped = True
            force[1] = self.mod_tracker.player_jump(PLAYER_JUMP_FORCE)
        self.physics_engine.apply_force(self.player, force)

        if not self.player.stationary and not self.current_steps:
            self.current_steps = sounds["steps"].play(loop=True)
        if self.player.stationary and self.current_steps:
            arcade.stop_sound(self.current_steps)
            self.current_steps = None
        for enemy in self.enemies:
            enemy.update_animation()
            if enemy.reached_boundry():
                enemy.direction = not enemy.direction
            if enemy.direction:  # direction = True -> Movement to the right
                self.physics_engine.apply_force(enemy, [300, 0])
            elif not enemy.direction:
                self.physics_engine.apply_force(enemy, [-300, 0])
        self.scroll_to()

    def scroll_to(self):
        y_pos = self.player.center_y - self.window.height / 2
        if y_pos < 0:
            y_pos = 0
        position = Vec2(0, y_pos)
        self.camera.move_to(position, 1)
