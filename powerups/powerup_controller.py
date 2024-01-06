from powerups.speed import Speed
from powerups.firerate import FireRate
from random import randint
from powerups.powerup import Powerup

class PowerupController:
    powerup_options = [
        {
            'class': Speed,
            'path': 'speed.png'
        },
        {
            'class': FireRate,
            'path': 'firerate.png'
        }
    ]
    
    def __init__(self, powerups, players, *groups):
        self.powerups = powerups
        self.players = players
        self.groups = groups
        
    def spawn_powerup(self, coords):
        powerup_index = randint(0, len(self.powerup_options) - 1)
        powerup = self.powerup_options[powerup_index]
        
        Powerup(powerup['class'], coords, self.players, self.powerups, powerup['path'], *self.groups)
