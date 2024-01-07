from abc import ABC, abstractmethod

class StatsPowerup(ABC):
    powerup_type = 'stats'
    
    def __init__(self, player, cooldown):
        self.cooldown = cooldown
        self.player = player
        self.instantiate()

    @abstractmethod
    def instantiate(self):
        pass
    
    def update(self):
        self.cooldown -= 1
        if self.cooldown < 0:
            self.remove()         
    
    @abstractmethod
    def remove(self):
        self.player.remove_stats_powerup(self)
