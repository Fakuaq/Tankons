from abc import ABC, abstractmethod


class ShotPowerup(ABC):
    powerup_type = 'shot'

    def __init__(self, player, cooldown, shot):
        self.cooldown = cooldown
        self.player = player
        self.shot = shot

    @abstractmethod
    def shoot(self):
        pass

    def update(self):
        if self.shot:
            self.cooldown -= 1
            if self.cooldown < 0:
                self.remove()

    def remove(self):
        self.player.remove_weapon_powerup()
