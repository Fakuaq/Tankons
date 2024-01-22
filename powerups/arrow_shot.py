from powerups.shot_powerup import ShotPowerup
import pygame as pg
from shot import Shot
from sound_controller import SoundController

class ArrowShot(ShotPowerup):
    """
    Powerup that allows the player to shoot multiple shots in a wide arrow shape.

    Attributes:
        - cooldown (int): The cooldown time between shots.
        - speed (int): The speed of the shots.
        - shot (bool): Flag to indicate that the powerup has been used.

    Methods:
        - __init__(self, player): Initializes the ArrowShot powerup for a specific player.
        - shoot(self): Overrides the shoot method to allow shots in a wide arrow shape.
    """
    cooldown = 20
    speed = 3
    # checks if the powerup has been used 
    shot = False
    
    def __init__(self, player):
        """
        Initializes the ArrowShot powerup for a specific player.

        Parameters:
            - player (Player): The player associated with this powerup.
        """
        super().__init__(player, self.cooldown, self.shot)
        self.angle_positive = self.player.angle
        self.angle_negative = self.player.angle
        
    def shoot(self):
        """
        Overrides the shoot method to allow shooting shots in a wider angle.

        Parameters:
            None

        Returns:
            None
        """
        if not self.shot:
            self.angle_positive = self.player.angle
            self.angle_negative = self.player.angle

        # Increment and decrement angles for a wider shot angle
        SoundController.powerup_arrowshot_sound()
        self.shot = True
        self.angle_positive += 1
        self.angle_negative -= 1
        
        # Reset angles if they exceed the specified range
        if self.angle_positive > self.player.angle + 10 or self.angle_negative < self.player.angle - 10:
            self.angle_positive = self.player.angle
            self.angle_negative = self.player.angle

        # Calculate directions for positive and negative angles
        direction_pos = pg.math.Vector2(0, 1).rotate(-self.angle_positive + 180)
        direction_neg = pg.math.Vector2(0, 1).rotate(-self.angle_negative + 180)
        
        # Spawn show with the calculated directions
        Shot(self.player, self.player.get_turret_position(), direction_pos, self.player.shot_bounces, 5.5, self.speed, self.player.walls, self.player.shots, self.player.groups)
        Shot(self.player, self.player.get_turret_position(), direction_neg, self.player.shot_bounces, 5.5, self.speed, self.player.walls, self.player.shots, self.player.groups)
            
        