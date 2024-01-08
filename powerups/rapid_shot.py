from powerups.shot_powerup import ShotPowerup
import pygame as pg
from shot import Shot
from sound_controller import SoundController

class RapidShot(ShotPowerup):
    """
    A powerup class that enables a rapid-fire shooting mode for a player.

    Attributes:
        cooldown (int): The cooldown duration for the rapid shot powerup.
        speed (int): The speed of the rapid shots.
        radius (int): The radius of the rapid shots.
        bounces (int): The number of times rapid shots can bounce off walls.
        shot (bool): Flag indicating whether the rapid shot mode is active.

    Methods:
        __init__(self, player): Initializes the RapidShot powerup for a given player.
        shoot(self): Overrides the shoot method to allow rapid-fire shots.
    """
    cooldown = 60
    speed = 8
    radius = 10
    bounces = 7
    shot = False

    def __init__(self, player):
        super().__init__(player, self.cooldown, self.shot)

    def shoot(self):
        """
        Overrides the shoot method to enable rapid-fire shooting mode.

        Parameters:
            None

        Returns:
            None
        """
        if not self.shot:
            # Set the shot flag to True, indicating that the shot is fired
            self.shot = True
            # Play the sound effect for the big shot powerup
            SoundController.powerup_bigshot_sound()
            # Calculate the direction vector for the shot based on player's angle
            direction = pg.math.Vector2(0, 1).rotate(-self.player.angle + 180)
            # Create a new Shot instance with specified parameters and add it to relevant groups
            Shot(self.player, self.player.get_turret_position(), direction, self.bounces, self.radius, self.speed, self.player.walls, self.player.shots, self.player.groups)
            
        