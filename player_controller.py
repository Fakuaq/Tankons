from config import controls
from player import Player

class PlayerController:
    def __init__(self, scores, walls, shots, players, all_sprites):
        self.scores = scores
        self.walls = walls
        self.shots = shots
        self.players = players
        self.all_sprites = all_sprites
        
    def spawn_players(self, count, coords):
        if count > len(controls):
            raise RuntimeError('Can\'t create more players than there are controls for')
            
        for i in range(count):
            Player(i + 1, self.scores[i + 1], controls[i], coords[i], self.shots, self.walls, self.players, self.all_sprites)

    def last_player_standing(self):
        if len(self.players) == 0: # if all players killed at the same frame
            return 0
        if len(self.players) == 1:
            return self.players.sprites()[0]
        
        return None
