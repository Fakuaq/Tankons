import pygame as pg
import random

class Particle(pg.sprite.Sprite):
    """
    A class representing a particle for visual effects in the game.

    Attributes:
        - image (pygame.Surface): The surface representing the particle.
        - lifetime (int): The lifespan of the particle in frames.
        - image (pygame.Surface): The surface used to represent the particle in the game.
        - rect (pygame.Rect): The rectangular area occupied by the particle on the game screen.
        - velocity (pygame.math.Vector2): Represent the velocity of the particle

    Methods:
        - __init__(self, x, y, color, speed, *groups):
            Initializes the Particle object with the specified parameters.

        - update(self):
            Updates the position and behavior of the particle.
    """
    image = pg.Surface((5, 5))
    lifetime = 20
        
    def __init__(self, x, y, color, speed, *groups):
        """
        Initializes the Particle object with the specified parameters.

        Parameters:
            - x (float): The initial x-coordinate of the particle.
            - y (float): The initial y-coordinate of the particle.
            - color (tuple): The RGB color tuple of the particle.
            - speed (float): The speed of the particle.
            - *groups: Sprite groups to which the particle should belong.
        """
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pg.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * speed
        
        pg.sprite.Sprite.__init__(self, *groups)
        
    def update(self):
        """
        Updates the position and behavior of the particle.

        Parameters:
            None

        Returns:
            None
        """
        self.rect.center += self.velocity
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
