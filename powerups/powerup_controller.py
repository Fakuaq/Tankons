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
        self.powerups = powerups
        self.players = players
        self.groups = groups
        self.walls = walls

    def spawn_powerup(self, coords):
        powerup_index = randint(0, len(self.powerup_options) - 1)
        powerup = self.powerup_options[powerup_index]

        powerup_sprite = Powerup(powerup['class'], powerup['path'], coords, self.players, self.powerups, self.walls,
                                 *self.groups)
        return powerup_sprite, powerup['class']

    def instantiate_powerup(self, powerup_type, coords):
        path = ''
        for powerup in self.powerup_options:
            if powerup['class'] == powerup_type:
                path = powerup['path']

        Powerup(powerup_type, path, coords, self.players, self.powerups, self.walls, *self.groups)
