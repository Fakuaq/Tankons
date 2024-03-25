from powerups.stats_powerup import StatsPowerup


class Speed(StatsPowerup):
    cooldown = 60 * 4

    def __init__(self, player):
        super().__init__(player, self.cooldown)

    def instantiate(self):
        self.player.speed *= 1.5

    def remove(self):
        self.player.speed /= 1.5
        super().remove()
