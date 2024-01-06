from shot import Shot
from particle import Particle
import pygame as pg
import math

class Player(pg.sprite.Sprite):
    speed = 3
    rotation_speed = 4
    shot_cd = 20
    curr_shot_cd = shot_cd
    angle = 0

    def __init__(self, identity, score, controls, pos, shots, walls, players, *groups):
        self.score = score
        self.identity = identity
        self.image = pg.image.load(f'assets/tank_{identity}.png').convert_alpha()
        self.image_copy = self.image
        self.controls = controls
        self.rect = self.image.get_rect(center=pos)
        self.shots = shots
        self.walls = walls
        self.player_color = self.get_sprite_color()
        self.players = players
        self.groups = groups

        pg.sprite.Sprite.__init__(self, self.players, *self.groups)

    def update(self):
        keys = pg.key.get_pressed()

        # rotate sprite
        rotation = int(keys[self.controls['rotate_left']] - keys[self.controls['rotate_right']])
        if rotation:
            self.angle = self.angle % 360 + rotation * self.rotation_speed
            self.image = pg.transform.rotate(self.image_copy, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

        # movement update
        direction = int(keys[self.controls['down']] - keys[self.controls['up']])
        direction_vector = pg.math.Vector2(0, 1).rotate(-self.angle) * direction * self.speed
        self.rect.center += direction_vector

        # shoot update
        self.curr_shot_cd -= 1
        if keys[self.controls['shoot']]:
            self.shoot()

        # shot collision        
        if pg.sprite.spritecollideany(self, self.shots):
            shot = pg.sprite.spritecollideany(self, self.shots)
            
            if shot.shot_by is not self or (shot.bounces != 3 and shot.shot_by is self):
                shot.kill()
                self.kill_player()

        # wall collision
        if pg.sprite.spritecollideany(self, self.walls):
            self.rect.center -= direction_vector

        # player collision
        if pg.sprite.spritecollide(self, self.players, False):
            players = pg.sprite.spritecollide(self, self.players, False)
            if self not in players:
                self.rect.center -= 1.1 * direction_vector

    def kill_player(self):
        particle_count = 50  
        particle_speed = 5
        particle_color = self.player_color

        for _ in range(particle_count):
            Particle(self.rect.centerx, self.rect.centery, particle_color, particle_speed, *self.groups)
            
        self.kill()
        
    def get_sprite_color(self):
        return self.image.get_at((int(self.rect.width / 2 + 5), int(self.rect.height / 2)))
    
    def get_turret_position(self, rotation_angle):
        x_turret = self.rect.centerx - (self.rect.height / 2) * math.sin(math.radians(rotation_angle))
        y_turret = self.rect.centery - (self.rect.height / 2) * math.cos(math.radians(rotation_angle))

        return int(x_turret), int(y_turret)
    
    def shoot(self):
        if self.curr_shot_cd > 0: return

        self.curr_shot_cd = self.shot_cd
        turret_position = self.get_turret_position(self.angle)
       
        direction = pg.math.Vector2(0, 1).rotate(-self.angle + 180)
        Shot(self, turret_position, direction, 5, self.walls, self.shots, *self.groups)
