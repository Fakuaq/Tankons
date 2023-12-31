import pygame as pg
from movement import Movement

class Shot(pg.sprite.Sprite, Movement):
    life_cd = 60 * 3
    current_life_cd = life_cd
    image = pg.Surface((10, 10))
    image.fill('black')
    
    def __init__(self, player, position, direction, speed, *groups):
        self.shot_by = player
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.direction = direction

        pg.sprite.Sprite.__init__(self, *groups)
        Movement.__init__(self, position, self.speed)

    def update(self):
        self.rect.center = self.move(self.direction)

        self.current_life_cd -= 1

        if self.current_life_cd <= 0:
            self.kill()
