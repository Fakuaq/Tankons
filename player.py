from shot import Shot
import pygame as pg
import math

class Player(pg.sprite.Sprite):
    speed = 3
    rotation_speed = 4
    shot_cd = 20
    curr_shot_cd = shot_cd
    angle = 0

    def __init__(self, pos, shots, walls, *groups):
        self.image = pg.image.load('assets/tank_1.png').convert_alpha()
        self.image_copy = self.image
        self.rect = self.image.get_rect(topleft=pos)
        self.shots = shots
        self.walls = walls

        pg.sprite.Sprite.__init__(self, *groups)

    def update(self):
        keys = pg.key.get_pressed()

        # rotate sprite
        rotation = int(keys[pg.K_LEFT] - keys[pg.K_RIGHT])
        if rotation:
            self.angle = self.angle % 360 + rotation * self.rotation_speed
            self.image = pg.transform.rotate(self.image_copy, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

        # movement update
        direction = int(keys[pg.K_DOWN] - keys[pg.K_UP])
        direction_vector = pg.math.Vector2(0, 1).rotate(-self.angle) * direction * self.speed
        self.rect.center += direction_vector

        # shoot update
        self.curr_shot_cd -= 1
        if pg.mouse.get_pressed()[0]:
            self.shoot()

        # collision detection        
        if pg.sprite.spritecollideany(self, self.shots):
            shot = pg.sprite.spritecollideany(self, self.shots)

            if shot.shot_by is not self:
                shot.kill()
                self.kill()

        if pg.sprite.spritecollideany(self, self.walls):
            self.rect.center -= direction_vector

    def get_turret_position(self, rotation_angle):
        x_turret = self.rect.centerx - (self.rect.height / 2) * math.sin(math.radians(rotation_angle))
        y_turret = self.rect.centery - (self.rect.height / 2) * math.cos(math.radians(rotation_angle))

        return int(x_turret), int(y_turret)
    
    def shoot(self):
        if self.curr_shot_cd > 0:
            return

        self.curr_shot_cd = self.shot_cd
        turret_position = self.get_turret_position(self.angle)
        mouse_x, mouse_y = pg.mouse.get_pos()
        direction = pg.math.Vector2(mouse_x - self.rect.centerx, mouse_y - self.rect.centery)
        if direction.magnitude() > 0:
            direction = direction.normalize() * 3
            Shot(self, turret_position, direction, 5, self.shots, *self.groups())
