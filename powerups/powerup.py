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
        - sprite_path (str): The path to the powerup sprite.
        - coords (tuple): The coordinates (x, y) of the powerup.
        - players (pygame.sprite.Group): The group of players in the game.
        - powerup_sprites (pygame.sprite.Group): The group of powerup sprites.
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
        super().__init__(powerup_sprites, *groups)
        self.powerup = powerup
        self.players = players
        self.powerup_sprites = powerup_sprites
        self.walls = walls

        self.image = pg.image.load(self.base_path + sprite_path).convert_alpha()
        self.rect = self.image.get_rect(center=coords)
        
    def update(self):
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
                    player.weapon_powerup = powerup
        