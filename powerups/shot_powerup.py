from abc import ABC, abstractmethod

class ShotPowerup(ABC):
    """
    An abstract base class representing a shot-related powerup for a player.

    Attributes:
        - powerup_type (str): The type of the powerup, set to 'shot'.

    Methods:
        - __init__(self, player, cooldown, shot):
            Initializes the ShotPowerup with the specified player, cooldown, and shot attributes.

        - shoot(self):
            Abstract method to define the behavior of shooting for the specific shot powerup.

        - update(self):
            Decrements the cooldown and removes the powerup if the cooldown reaches zero.

        - remove(self):
            Removes the powerup effect from the player.
    """
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
