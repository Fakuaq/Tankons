from shot import Shot
from movement import Movement
import pygame as pg


class Player(pg.sprite.Sprite, Movement):
    image = pg.Surface((32, 32))
    image.fill((0, 125, 200))
    speed = 4
    shot_cd = 20
    curr_shot_cd = shot_cd

    def __init__(self, pos, shots, walls, *groups):
        self.rect = self.image.get_rect(topleft=pos)
        self.shots = shots
        self.walls = walls

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
        if pg.sprite.spritecollideany(self, self.shots):
            shot = pg.sprite.spritecollideany(self, self.shots)

            if shot.shot_by is not self:
                shot.kill()
                self.kill()

        if pg.sprite.spritecollideany(self, self.walls):
            walls = pg.sprite.spritecollide(self, self.walls, False)
            new_coords = pg.math.Vector2((self.rect.centerx, self.rect.centery))

            for wall in walls:
                if abs(wall.rect.left - self.rect.right) <= self.speed:
                    new_coords.x = wall.rect.left - self.rect.size[0] / 2
                elif abs(wall.rect.right - self.rect.left) <= self.speed:
                    new_coords.x = wall.rect.right + self.rect.size[0] / 2

                if abs(wall.rect.top - self.rect.bottom) <= self.speed:
                    new_coords.y = wall.rect.top - self.rect.size[1] / 2
                elif abs(wall.rect.bottom - self.rect.top) <= self.speed:
                    new_coords.y = wall.rect.bottom + self.rect.size[1] / 2

                self.rect.center = self.reset_move(new_coords)

    def shoot(self):
        if self.curr_shot_cd > 0:
            return

        self.curr_shot_cd = self.shot_cd

        mouse_x, mouse_y = pg.mouse.get_pos()
        direction = pg.math.Vector2(mouse_x - self.rect.centerx, mouse_y - self.rect.centery)
        if direction.magnitude() > 0:
            direction = direction.normalize() * 3
            Shot(self, self.rect.center, direction, 5, self.shots, *self.groups())
