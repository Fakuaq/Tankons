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

        collided_wall = pg.sprite.spritecollideany(self, self.walls)
        if collided_wall:
            overlap_top = abs(self.rect.bottom - collided_wall.rect.top)
            overlap_bottom = abs(self.rect.top - collided_wall.rect.bottom)
            overlap_left = abs(self.rect.right - collided_wall.rect.left)
            overlap_right = abs(self.rect.left - collided_wall.rect.right)

            smallest_overlap = min(overlap_top, overlap_bottom, overlap_left, overlap_right)

            if smallest_overlap == overlap_top:
                self.direction.y *= -1
                self.rect.bottom = collided_wall.rect.top
            elif smallest_overlap == overlap_bottom:
                self.direction.y *= -1
                self.rect.top = collided_wall.rect.bottom
            elif smallest_overlap == overlap_left:
                self.direction.x *= -1
                self.rect.right = collided_wall.rect.left
            elif smallest_overlap == overlap_right:
                self.direction.x *= -1
                self.rect.left = collided_wall.rect.right

            if self.bounces == self.max_bounces:
                return self.kill()
            
            self.position.update(self.rect.centerx, self.rect.centery)
            self.bounces += 1
