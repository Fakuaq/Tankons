import pygame as pg

class Shot(pg.sprite.Sprite):
    life_cd = 60 * 3
    current_life_cd = life_cd
    bullet_radius = 5
    image = pg.Surface((bullet_radius * 2, bullet_radius * 2), pg.SRCALPHA)
    pg.draw.circle(image, "black", (bullet_radius, bullet_radius), bullet_radius)

    def __init__(self, player, position, direction, speed, *groups):
        self.shot_by = player
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.direction = direction

        pg.sprite.Sprite.__init__(self, *groups)

    def update(self):
        # movement
        direction_normalized = self.direction.normalize() * self.speed
        self.rect.center += direction_normalized

        # life cd
        self.current_life_cd -= 1
        if self.current_life_cd <= 0:
            self.kill()
