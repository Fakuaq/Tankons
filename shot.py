import pygame as pg

class Shot(pg.sprite.Sprite):
    life_cd = 60 * 3
    current_life_cd = life_cd
    bounces = 0

    def __init__(self, player, position, direction, max_bounces, radius, speed, walls, *groups):
        self.shot_by = player
        self.max_bounces = max_bounces
        self.speed = speed
        self.radius = radius
        self.speed = speed
        self.direction = direction
        self.walls = walls
        self.image = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
        pg.draw.circle(self.image, "black", (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=position)
        self.position = pg.math.Vector2((self.rect.centerx, self.rect.centery))
        
        pg.sprite.Sprite.__init__(self, *groups)

    def update(self):
        # movement
        direction_normalized = self.direction.normalize() * self.speed
        self.position += direction_normalized
        self.rect.center = int(self.position.x), int(self.position.y)

        # life cd
        self.current_life_cd -= 1
        if self.current_life_cd <= 0:
            self.kill()

        collided_walls = pg.sprite.spritecollide(self, self.walls, False)
        for wall in collided_walls:
            if self.rect.centerx < wall.rect.left:
                self.direction.x *= -1
                self.rect.right = wall.rect.left
                self.bounces += 1
                if self.bounces == self.max_bounces:
                    return self.kill()
                break
            if self.rect.centerx > wall.rect.right:
                self.direction.x *= -1
                self.rect.left = wall.rect.right
                self.bounces += 1
                if self.bounces == self.max_bounces:
                    return self.kill()
                break
            if self.rect.centery < wall.rect.top:
                self.direction.y *= -1
                self.rect.bottom = wall.rect.top
                self.bounces += 1
                if self.bounces == self.max_bounces:
                    return self.kill()
                break
            if self.rect.centery > wall.rect.bottom:
                self.direction.y *= -1
                self.rect.top = wall.rect.bottom
                self.bounces += 1
                if self.bounces == self.max_bounces:
                    return self.kill()
                break
                