from shot import Shot
from particle import Particle
from sound_controller import SoundController
import pygame as pg
import math
from observers.game_event_observable import GameEventObservable
from enums.game_event import GameEvent


class Player(pg.sprite.Sprite):
    speed = 3
    rotation_speed = 3
    shot_bounces = 3
    shot_radius = 5.5
    shot_speed = 5
    shot_cd = 20
    curr_shot_cd = shot_cd
    angle = 0
    stats_powerups = []
    weapon_powerup = None
    last_inputs = None
    rotation = 0
    direction = 0
    base_path = 'assets/players/'


    def __init__(self, identity, score, controls, pos, shots, walls, players, player_controlling, *groups):
        self.score = score
        self.identity = identity
        self.image = pg.image.load(f'{self.base_path}tank_{identity}.png').convert_alpha()
        self.image_copy = self.image
        self.controls = controls
        self.rect = self.image.get_rect(center=pos)
        self.position = pg.math.Vector2((self.rect.centerx, self.rect.centery))
        self.shots = shots
        self.walls = walls
        self.player_color = self.get_sprite_color()
        self.players = players
        self.groups = groups
        self.player_controlling = player_controlling

        pg.sprite.Sprite.__init__(self, self.players, *self.groups)

    def update(self):
        keys = pg.key.get_pressed()

        # movement update
        self.rect.center = int(self.position.x), int(self.position.y)
        self.image = pg.transform.rotate(self.image_copy, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.player_controlling:
            self.direction = int(keys[self.controls['down']] - keys[self.controls['up']])
            self.rotation = int(keys[self.controls['rotate_left']] - keys[self.controls['rotate_right']])

            if self.last_inputs != (self.direction, self.rotation):
                GameEventObservable().set_game_event((GameEvent.COORDS, (self.direction, self.rotation)))
            self.last_inputs = (self.direction, self.rotation)

        # update position
        direction_vector = pg.math.Vector2(0, 1).rotate(-self.angle) * self.direction * self.speed
        self.position += direction_vector

        # rotate sprite
        rotation = self.rotation if self.direction != 1 else self.rotation * -1  # flip rotation if moving backwards
        if rotation:
            self.angle = self.angle % 360 + rotation * self.rotation_speed
            self.rect = self.image.get_rect(center=self.rect.center)

        # shoot update
        self.curr_shot_cd -= 1
        if keys[self.controls['shoot']] and self.player_controlling:
            if self.curr_shot_cd <= 0:
                self.shoot()
                self.curr_shot_cd = self.shot_cd
                GameEventObservable().set_game_event((GameEvent.SHOT, self.identity))

        # shot collision        
        if pg.sprite.spritecollideany(self, self.shots):
            shot = pg.sprite.spritecollideany(self, self.shots)

            if shot.shot_by is not self or (shot.bounces != 0 and shot.shot_by is self):
                shot.kill()
                self.kill_player()

        # wall collision
        for collided_wall in pg.sprite.spritecollide(self, self.walls, False):
            overlap_top = abs(self.rect.bottom - collided_wall.rect.top)
            overlap_bottom = abs(self.rect.top - collided_wall.rect.bottom)
            overlap_left = abs(self.rect.right - collided_wall.rect.left)
            overlap_right = abs(self.rect.left - collided_wall.rect.right)

            smallest_overlap = min(overlap_top, overlap_bottom, overlap_left, overlap_right)

            if smallest_overlap == overlap_top:
                self.rect.bottom = collided_wall.rect.top
            elif smallest_overlap == overlap_bottom:
                self.rect.top = collided_wall.rect.bottom
            elif smallest_overlap == overlap_left:
                self.rect.right = collided_wall.rect.left
            elif smallest_overlap == overlap_right:
                self.rect.left = collided_wall.rect.right

            self.position.update(self.rect.centerx, self.rect.centery)

        # player collision
        if pg.sprite.spritecollide(self, self.players, False) and self.player_controlling:
            players = pg.sprite.spritecollide(self, self.players, False)
            for player in players:
                if player is not self:
                    self.position -= 1.1 * direction_vector
                    self.rect.center = int(self.position.x), int(self.position.y)

        # powerup update
        for powerup in self.stats_powerups.copy():
            powerup.update()
        if self.weapon_powerup:
            self.weapon_powerup.update()

    def kill_player(self):
        particle_count = 50
        particle_speed = 5
        particle_color = self.player_color
        SoundController.death_sound()

        for _ in range(particle_count):
            Particle(self.rect.centerx, self.rect.centery, particle_color, particle_speed, *self.groups)

        self.kill()

    def get_sprite_color(self):
        return self.image.get_at((int(self.rect.width / 2 + 5), int(self.rect.height / 2)))

    def get_turret_position(self):
        x_turret = self.rect.centerx - (self.rect.height / 2) * math.sin(math.radians(self.angle))
        y_turret = self.rect.centery - (self.rect.height / 2) * math.cos(math.radians(self.angle))

        return int(x_turret), int(y_turret)

    def shoot(self):
        if self.weapon_powerup:
            self.weapon_powerup.shoot()
        else:
            turret_position = self.get_turret_position()

            direction = pg.math.Vector2(0, 1).rotate(-self.angle + 180)
            Shot(self, turret_position, direction, self.shot_bounces, self.shot_radius, self.shot_speed, self.walls, self.shots, *self.groups)
            SoundController.shoot_sound()

    def add_stats_powerup(self, powerup):
        self.stats_powerups.append(powerup)

    def remove_stats_powerup(self, powerup):
        self.stats_powerups.remove(powerup)

    def add_weapon_powerup(self, powerup):
        self.weapon_powerup = powerup

    def remove_weapon_powerup(self):
        self.weapon_powerup = None
