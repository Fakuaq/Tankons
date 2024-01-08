from abc import ABC, abstractmethod

class StatsPowerup(ABC):
    """
    Abstract base class for player stats powerups in the game.

    Attributes:
        - powerup_type (str): A string indicating the type of powerup (set to 'stats').
        - cooldown (int): The cooldown duration for the powerup.
        - player: The player instance that the powerup gets applied to.

    Methods:
        - __init__(self, player, cooldown):
            Initializes the StatsPowerup with the specified player and cooldown.

        - instantiate(self):
            Abstract method to be implemented by subclasses for initializing the powerup.

        - update(self):
            Updates the powerup state, including reducing the cooldown. It triggers removal when the cooldown reaches zero.

        - remove(self):
            Abstract method to be implemented by subclasses for removing the powerup effect from the player.
    """
    powerup_type = 'stats'
    
    def __init__(self, player, cooldown):
        """
        Initializes the StatsPowerup with the specified player and cooldown.

        Parameters:
            - player: The player instance associated with the powerup.
            - cooldown (int): The cooldown duration for the powerup.
        """
        self.cooldown = cooldown
        self.player = player
        self.instantiate()

    @abstractmethod
    def instantiate(self):
        """
        Abstract method to be implemented by subclasses for initializing the powerup.

        Parameters:
            None

        Returns:
            None
        """
        pass
    
    def update(self):
        """
        Updates the powerup state, including decerementing the cooldown. It triggers removal when the cooldown reaches zero.

        Parameters:
            None

        Returns:
            None
        """
        self.cooldown -= 1
        if self.cooldown < 0:
            self.remove()         
    
    @abstractmethod
    def remove(self):
        """
        Abstract method to be implemented by subclasses for removing the powerup effect from the player.

        Parameters:
            None

        Returns:
            None
        """
        self.player.remove_stats_powerup(self)
