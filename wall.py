import pygame as pg


class Wall(pg.sprite.Sprite):
    def __init__(self, pos, size, *groups):
        self.image = pg.Surface(size)
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)

        super().__init__(*groups)
