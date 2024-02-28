from powerups.stats_powerup import StatsPowerup


class FireRate(StatsPowerup):
    cooldown = 60 * 4

    def __init__(self, player):
        super().__init__(player, self.cooldown)

    def instantiate(self):
        self.player.shot_cd /= 2

    def remove(self):
        self.player.shot_cd *= 2
        super().remove()
