from powerups.speed import Speed
from powerups.firerate import FireRate
from random import randint
from powerups.powerup import Powerup
from powerups.arrow_shot import ArrowShot
from powerups.rapid_shot import RapidShot

class PowerupController:
    powerup_options = [
        {
            'class': Speed,
            'path': 'speed.png',
            'type': 'stats'
        },
        {
            'class': FireRate,
            'path': 'firerate.png',
            'type': 'stats'
        },
        {
            'class': ArrowShot,
            'path': 'arrow_shot.png',
            'type': 'shot'
        },
        {
            'class': RapidShot,
            'path': 'rapid_shot.png',
            'type': 'shot'
        }
    ]
    
    def __init__(self, powerups, players, walls, *groups):
        self.powerups = powerups
        self.players = players
        self.groups = groups
        self.walls = walls
        
    def spawn_powerup(self, coords):
        powerup_index = randint(0, len(self.powerup_options) - 1)
        powerup = self.powerup_options[powerup_index]
        
        Powerup(powerup['class'], powerup['type'], powerup['path'], coords, self.players, self.powerups, self.walls, *self.groups)
