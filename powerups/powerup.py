import pygame as pg
from powerups.stats_powerup import StatsPowerup
from powerups.shot_powerup import ShotPowerup
from typing import Type
from sound_controller import SoundController

class Powerup(pg.sprite.Sprite):
    base_path = 'assets/powerups/'
    
    def __init__(self, powerup: Type[StatsPowerup|ShotPowerup], powerup_type, sprite_path, coords, players, powerup_sprites, walls, *groups):
        super().__init__(powerup_sprites, *groups)
        self.powerup = powerup
        self.players = players
        self.powerup_sprites = powerup_sprites
        self.walls = walls
        self.powerup_type = powerup_type

        self.image = pg.image.load(self.base_path + sprite_path).convert_alpha()
        self.rect = self.image.get_rect(center=coords)
        
    def update(self):
        for player in self.players:
            collided_powerup = pg.sprite.spritecollideany(player, self.powerup_sprites)
            if collided_powerup:
                powerup = collided_powerup.powerup(player) # instantiate powerup
                collided_powerup.kill()
                SoundController.powerup_sound()
                
                if self.powerup_type == 'stats':
                    player.add_stats_powerup(powerup)
                elif self.powerup_type == 'shot':
                    player.weapon_powerup = powerup
        