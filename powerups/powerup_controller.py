from powerups.speed import Speed
from powerups.firerate import FireRate
from random import randint
from powerups.powerup import Powerup
from powerups.arrow_shot import ArrowShot
from powerups.rapid_shot import RapidShot

class PowerupController:
    """
    A class responsible for controlling the spawning of powerups in the game.

    Attributes:
        - powerups (pygame.sprite.Group): Sprite group for powerups.
        - players (pygame.sprite.Group): Sprite group for players.
        - groups (tuple): Additional sprite groups to which powerups should belong.
        - walls (pygame.sprite.Group): Sprite group for walls.
        - powerup_options (list): defines possible powerup classes and sprites for each powerup.

    Methods:
        - spawn_powerup(self, coords):
            Spawns a random powerup at the specified coordinates.
    """
    powerup_options = [
        {
            'class': Speed,
            'path': 'speed.png',
        },
        {
            'class': FireRate,
            'path': 'firerate.png',
        },
        {
            'class': ArrowShot,
            'path': 'arrow_shot.png',
        },
        {
            'class': RapidShot,
            'path': 'rapid_shot.png',
        }
    ]
    
    def __init__(self, powerups, players, walls, *groups):
        """
        Initializes the PowerupController object with the specified parameters.

        Parameters:
            - powerups (pygame.sprite.Group): Sprite group for powerups.
            - players (pygame.sprite.Group): Sprite group for players.
            - walls (pygame.sprite.Group): Sprite group for walls.
            - *groups: Additional sprite groups to which powerups should belong.
        """
        self.powerups = powerups
        self.players = players
        self.groups = groups
        self.walls = walls
        
    def spawn_powerup(self, coords):
        """
        Spawns a random powerup at the specified coordinates.

        Parameters:
            - coords (tuple): The (x, y) coordinates where the powerup should be spawned.
        """
        powerup_index = randint(0, len(self.powerup_options) - 1)
        powerup = self.powerup_options[powerup_index]
        
        Powerup(powerup['class'], powerup['path'], coords, self.players, self.powerups, self.walls, *self.groups)
