import pygame as pg
from powerups.stats_powerup import StatsPowerup
from powerups.shot_powerup import ShotPowerup
from typing import Type
from sound_controller import SoundController

class Powerup(pg.sprite.Sprite):
    """
    A class representing a powerup in the game.

    Attributes:
        - base_path (str): The base path for loading powerup sprites.
        - powerup (StatsPowerup|ShotPowerup): The type of powerup to be applied.
        - players (pygame.sprite.Group): The group of players in the game.
        - powerup_sprites (pygame.sprite.Group): The group of powerup sprites.
        - image (pygame.Surface): The surface used to represent the powerup in the game.
        - rect (pygame.Rect): The rectangular area occupied by the powerup on the game screen.
        - walls (pygame.sprite.Group): The group of wall sprites.
        - *groups: Additional sprite groups to which the powerup should belong.

    Methods:
        - __init__(self, powerup: Type[StatsPowerup|ShotPowerup], sprite_path, coords, players, powerup_sprites, walls, *groups):
            Initializes the Powerup object with the specified parameters.

        - update(self):
            Updates the state of the powerup in the game.
    """
    base_path = 'assets/powerups/'
    
    def __init__(self, powerup: Type[StatsPowerup|ShotPowerup], sprite_path, coords, players, powerup_sprites, walls, *groups):
        """
        Initializes the Powerup object.

        Parameters:
            - powerup (Type[StatsPowerup|ShotPowerup]): The type of powerup class associated with this instance.
            - sprite_path (str): The file path for the sprite image.
            - coords (tuple): The coordinates (x, y) where the powerup will be placed.
            - players (pygame.sprite.Group): The group of players in the game.
            - powerup_sprites (pygame.sprite.Group): The group of powerup sprites in the game.
            - walls (pygame.sprite.Group): The group of wall sprites in the game.
            - *groups: Additional sprite groups to which the powerup should belong.
        """
        self.powerup = powerup
        self.players = players
        self.powerup_sprites = powerup_sprites
        self.walls = walls

        self.image = pg.image.load(self.base_path + sprite_path).convert_alpha()
        self.rect = self.image.get_rect(center=coords)

        super().__init__(powerup_sprites, *groups)
        
    def update(self):
        """
        Updates the powerup and checks for collisions with players.

        Parameters:
            None

        Returns:
            None
        """
        for player in self.players:
            # check player and powerup collision
            collided_powerup = pg.sprite.spritecollideany(player, self.powerup_sprites)
            if collided_powerup:
                powerup = collided_powerup.powerup(player) # instantiate powerup
                collided_powerup.kill()
                SoundController.powerup_sound()
                
                if powerup.powerup_type == 'stats':
                    player.add_stats_powerup(powerup)
                elif powerup.powerup_type == 'shot':
                    player.add_weapon_powerup(powerup)
        