from powerups.stats_powerup import StatsPowerup

class Speed(StatsPowerup):
    """
    A class representing the Speed powerup, which increases the player's movement speed.

    Attributes:
        - cooldown (int): The cooldown duration for the powerup.

    Methods:
        - __init__(self, player):
            Initializes the Speed powerup with the specified player.

        - instantiate(self):
            Initializes the powerup effect by multiplying the player's speed.

        - remove(self):
            Removes the powerup effect by dividing the player's speed. Calls the superclass method for removal.
    """
    cooldown = 60 * 4
    
    def __init__(self, player):
        """
        Initializes the Speed powerup with the specified player.

        Parameters:
            - player: The player instance that the powerup gets applied to.
        """
        super().__init__(player, self.cooldown)
    
    def instantiate(self):
        """
        Initializes the powerup effect by multiplying the player's speed.

        Parameters:
            None

        Returns:
            None
        """
        self.player.speed *= 1.5
    
    def remove(self):
        """
        Removes the powerup effect by dividing the player's speed. Calls the superclass method for removal.

        Parameters:
            None

        Returns:
            None
        """
        self.player.speed /= 1.5
        super().remove()