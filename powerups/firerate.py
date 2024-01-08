from powerups.stats_powerup import StatsPowerup

class FireRate(StatsPowerup):
    """
    A powerup class that modifies the firing rate of a player's shots.

    Attributes:
        cooldown (int): The cooldown duration for the powerup effect.

    Methods:
        __init__(self, player): Initializes the FireRate powerup for a given player.
        instantiate(self): Applies the FireRate powerup to the player by reducing shot cooldown.
        remove(self): Removes the FireRate powerup from the player by restoring the shot cooldown.
    """
    cooldown = 60 * 4

    def __init__(self, player):
        """
        Initializes the FireRate powerup.

        Parameters:
            player (Player): The player object to apply the powerup to.

        Returns:
            None
        """
        super().__init__(player, self.cooldown)

    def instantiate(self):
        """
        Applies the FireRate powerup to the player by reducing shot cooldown.

        Parameters:
            None

        Returns:
            None
        """
        self.player.shot_cd /= 2

    def remove(self):
        """
        Removes the FireRate powerup from the player by restoring the shot cooldown.

        Parameters:
            None

        Returns:
            None
        """
        self.player.shot_cd *= 2
        super().remove()