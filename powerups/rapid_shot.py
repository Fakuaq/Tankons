from powerups.shot_powerup import ShotPowerup
import pygame as pg
from shot import Shot

class RapidShot(ShotPowerup):
    cooldown = 60
    speed = 8
    radius = 10
    bounces = 7
    shot = False

    def __init__(self, player):
        super().__init__(player, self.cooldown, self.shot)

    def shoot(self):
        if not self.shot:
            self.shot = True
            direction = pg.math.Vector2(0, 1).rotate(-self.player.angle + 180)
            Shot(self.player, self.player.get_turret_position(), direction, self.bounces, self.radius, self.speed, self.player.walls, self.player.shots, self.player.groups)
            
        