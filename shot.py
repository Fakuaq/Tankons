import pygame as pg

class Shot(pg.sprite.Sprite):
    """
    A class representing a projectile shot by a player.

    Attributes:
        - life_cd (int): The lifespan of the shot in frames.
        - current_life_cd (int): The current remaining lifespan of the shot.
        - bounces (int): The number of times the shot has bounced off walls.
        - shot_by (Player): The player who shot the projectile.
        - max_bounces (int): The maximum number of times the shot can bounce off walls.
        - speed (int): The speed of the shot.
        - radius (int): The radius of the shot.
        - direction (pygame.math.Vector2): The initial direction vector of the shot.
        - walls (Wall): The group of walls the shot can collide with.
        - image (pygame.Surface): The surface used to represent the shot in the game.
        - rect (pygame.Rect): The rectangular area occupied by the shot on the game screen.
        - position (pygame.math.Vector2): The current position of the shot.

    Methods:
        - __init__(self, player, position, direction, max_bounces, radius, speed, walls, *groups):
            Initializes the Shot object with the specified parameters.

        - update(self):
            Updates the position and behavior of the shot.
    """
    
    life_cd = 60 * 3
    current_life_cd = life_cd
    bounces = 0

    def __init__(self, player, position, direction, max_bounces, radius, speed, walls, *groups):
        """
        Initializes the Shot object with the specified parameters.

        Parameters:
            - player (Player): The player who shot the projectile.
            - position (tuple): The initial position of the shot (x, y).
            - direction (pygame.math.Vector2): The initial direction vector of the shot.
            - max_bounces (int): The maximum number of times the shot can bounce off walls.
            - radius (int): The radius of the shot.
            - speed (int): The speed of the shot.
            - walls (Wall): The group of walls the shot can collide with.
            - *groups: Sprite groups to which the shot should belong.
        """
        
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
        """
        Updates the position and behavior of the shot.

        This method is called each frame to update the shot's position and handle
        collisions with walls. The shot's lifespan is also decremented, and the shot
        is killed if it exceeds the maximum number of bounces.
        """
        # movement
        direction_normalized = self.direction.normalize() * self.speed
        self.position += direction_normalized
        self.rect.center = int(self.position.x), int(self.position.y)

        # life cd decremention
        self.current_life_cd -= 1
        if self.current_life_cd <= 0:
            self.kill()

        # collision
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
                self.kill()
                return

            self.position.update(self.rect.centerx, self.rect.centery)
            self.bounces += 1
