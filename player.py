from shot import Shot
from movement import Movement
import pygame as pg

class Player(pg.sprite.Sprite, Movement):
    def __init__(self, pos, player_shots, *groups):
        self.image = pg.Surface((32, 32))
        self.image.fill((0, 125, 200))
        self.rect = self.image.get_rect(center=pos)
        self.speed = 4
        self.shot_cd = 20
        self.curr_shot_cd = self.shot_cd
        self.player_shots = player_shots

        pg.sprite.Sprite.__init__(self, *groups)
        Movement.__init__(self, self.rect.center, self.speed)

    def update(self):
        # movement update
        keys = pg.key.get_pressed()
        direction_vector = pg.math.Vector2(keys[pg.K_RIGHT] - keys[pg.K_LEFT],
                                           keys[pg.K_DOWN] - keys[pg.K_UP])
        self.rect.center = self.move(direction_vector)

        # shoot update
        self.curr_shot_cd -= 1
        if pg.mouse.get_pressed()[0]:
            self.shoot()

        # collision detection        
        if pg.sprite.spritecollideany(self, self.player_shots):
            shot = pg.sprite.spritecollideany(self, self.player_shots)

            if shot.shot_by is not self:
                shot.kill()
                self.kill()
                

    def shoot(self):
        if self.curr_shot_cd > 0:
            return
        
        self.curr_shot_cd = self.shot_cd

        mouse_x, mouse_y = pg.mouse.get_pos()
        direction = pg.math.Vector2(mouse_x - self.rect.centerx, mouse_y - self.rect.centery)
        if direction.magnitude() > 0:
            direction = direction.normalize() * 3
            Shot(self, self.rect.center, direction, 5, self.player_shots, *self.groups())
