import pygame as pg
import random

class Particle(pg.sprite.Sprite):
    image = pg.Surface((5, 5))
    lifetime = 20
        
    def __init__(self, x, y, color, speed, *groups):
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pg.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * speed
        
        pg.sprite.Sprite.__init__(self, *groups)
        
    def update(self):
        self.rect.center += self.velocity
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
