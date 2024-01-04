import pygame as pg

class Shot(pg.sprite.Sprite):
    life_cd = 60 * 3
    current_life_cd = life_cd
    bullet_radius = 5.5
    bounces = 3
    image = pg.Surface((bullet_radius * 2, bullet_radius * 2), pg.SRCALPHA)
    pg.draw.circle(image, "black", (bullet_radius, bullet_radius), bullet_radius)

    def __init__(self, player, position, direction, speed, walls, *groups):
        self.shot_by = player
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.direction = direction
        self.walls = walls

        pg.sprite.Sprite.__init__(self, *groups)

    def update(self):
        # movement
        direction_normalized = self.direction.normalize() * self.speed
        self.rect.center += direction_normalized

        # life cd
        self.current_life_cd -= 1
        if self.current_life_cd <= 0:
            self.kill()

        collided_walls = pg.sprite.spritecollide(self, self.walls, False)
        for wall in collided_walls:
            if self.rect.centerx < wall.rect.left:
                self.direction.x *= -1
                self.rect.right = wall.rect.left
                self.bounces -= 1
                if self.bounces == 0:
                    return self.kill()
                break
            if self.rect.centerx > wall.rect.right:
                self.direction.x *= -1
                self.rect.left = wall.rect.right
                self.bounces -= 1
                if self.bounces == 0:
                    return self.kill()
                break
            if self.rect.centery < wall.rect.top:
                self.direction.y *= -1
                self.rect.bottom = wall.rect.top
                self.bounces -= 1
                if self.bounces == 0:
                    return self.kill()
                break
            if self.rect.centery > wall.rect.bottom:
                self.direction.y *= -1
                self.rect.top = wall.rect.bottom
                self.bounces -= 1
                if self.bounces == 0:
                    return self.kill()
                break