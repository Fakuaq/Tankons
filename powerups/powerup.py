import pygame as pg
from powerups.stats_powerup import StatsPowerup
from typing import Type

class Powerup(pg.sprite.Sprite):
    base_path = 'assets/powerups/'
    
    def __init__(self, powerup: Type[StatsPowerup], coords, players, powerups, sprite_path, *groups):
        super().__init__(powerups, *groups)
        self.powerup = powerup
        self.players = players
        self.powerups = powerups

        self.image = pg.image.load(self.base_path + sprite_path).convert_alpha()
        self.rect = self.image.get_rect(center=coords)
        
    def update(self):
        for player in self.players:
            collided_powerup = pg.sprite.spritecollideany(player, self.powerups)
            if collided_powerup:
                powerup = collided_powerup.powerup(player) # instantiate powerup
                player.add_stats_powerup(powerup)
                collided_powerup.kill()
        