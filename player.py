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

    def __init__(self, identity, controls, pos, shots, walls, particles, *groups):
        self.image = pg.image.load(f'assets/tank_{identity}.png').convert_alpha()
        self.controls = controls
        self.image_copy = self.image
        self.rect = self.image.get_rect(topleft=pos)
        self.shots = shots
        self.walls = walls
        self.particles = particles

        pg.sprite.Sprite.__init__(self, *groups)

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

        # collision detection        
        if pg.sprite.spritecollideany(self, self.shots):
            shot = pg.sprite.spritecollideany(self, self.shots)
            
            if shot.shot_by is not self:
                shot.kill()
                self.kill_player()

        if pg.sprite.spritecollideany(self, self.walls):
            self.rect.center -= direction_vector

    def kill_player(self):
        particle_count = 50  
        particle_speed = 5
        particle_color = self.get_sprite_color()

        for _ in range(particle_count):
            particle = Particle(self.rect.centerx, self.rect.centery, particle_color, particle_speed, self.particles, *self.groups())
            self.particles.add(particle)
            
        self.kill()
        
    def get_sprite_color(self):
        return self.image.get_at((int(self.rect.width / 2), int(self.rect.height / 2)))
    
    def get_turret_position(self, rotation_angle):
        x_turret = self.rect.centerx - (self.rect.height / 2) * math.sin(math.radians(rotation_angle))
        y_turret = self.rect.centery - (self.rect.height / 2) * math.cos(math.radians(rotation_angle))

        return int(x_turret), int(y_turret)
    
    def shoot(self):
        if self.curr_shot_cd > 0: return

        self.curr_shot_cd = self.shot_cd
        turret_position = self.get_turret_position(self.angle)
        mouse_x, mouse_y = pg.mouse.get_pos()
        direction = pg.math.Vector2(mouse_x - self.rect.centerx, mouse_y - self.rect.centery)
        if direction.magnitude() > 0:
            direction = pg.math.Vector2(0, 1).rotate(-self.angle + 180)
            Shot(self, turret_position, direction, 5, self.shots, *self.groups())
