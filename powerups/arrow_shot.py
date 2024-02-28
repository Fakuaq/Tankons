from powerups.shot_powerup import ShotPowerup
import pygame as pg
from shot import Shot
from sound_controller import SoundController


class ArrowShot(ShotPowerup):
    cooldown = 20
    speed = 3
    shot = False
    
    def __init__(self, player):
        super().__init__(player, self.cooldown, self.shot)
        self.angle_positive = self.player.angle
        self.angle_negative = self.player.angle
        
    def shoot(self):
        if not self.shot:
            self.angle_positive = self.player.angle
            self.angle_negative = self.player.angle
            self.shot = True
            SoundController.powerup_arrowshot_sound()

    def update(self):
        if not self.shot: return
        super().update()

        self.angle_positive += 1
        self.angle_negative -= 1

        if self.angle_positive > self.player.angle + 10 or self.angle_negative < self.player.angle - 10:
            self.angle_positive = self.player.angle
            self.angle_negative = self.player.angle

        direction_pos = pg.math.Vector2(0, 1).rotate(-self.angle_positive + 180)
        direction_neg = pg.math.Vector2(0, 1).rotate(-self.angle_negative + 180)

        Shot(self.player, self.player.get_turret_position(), direction_pos, self.player.shot_bounces, 5.5, self.speed,
             self.player.walls, self.player.shots, self.player.groups)
        Shot(self.player, self.player.get_turret_position(), direction_neg, self.player.shot_bounces, 5.5, self.speed,
             self.player.walls, self.player.shots, self.player.groups)
