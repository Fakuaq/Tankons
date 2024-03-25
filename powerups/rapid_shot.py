from powerups.shot_powerup import ShotPowerup
import pygame as pg
from shot import Shot
from sound_controller import SoundController


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
            # Set the shot flag to True, indicating that the shot is fired
            self.shot = True
            # Play the sound effect for the big shot powerup
            SoundController.powerup_bigshot_sound()
            # Calculate the direction vector for the shot based on player's angle
            direction = pg.math.Vector2(0, 1).rotate(-self.player.angle + 180)
            # Create a new Shot instance with specified parameters and add it to relevant groups
            Shot(self.player, self.player.get_turret_position(), direction, self.bounces, self.radius, self.speed,
                 self.player.walls, self.player.shots, self.player.groups)
