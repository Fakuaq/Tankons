from config import controls
from player import Player
import pygame as pg
pg.font.init()

class PlayerController:
    player_colors = {}
    font = pg.font.SysFont("San Francisco", 30)
    
    def __init__(self, screen, scores, walls, shots, players, all_sprites):
        self.screen = screen
        self.scores = scores
        self.walls = walls
        self.shots = shots
        self.players = players
        self.all_sprites = all_sprites
        
    def spawn_players(self, count, coords):
        if count > len(controls):
            raise RuntimeError('Can\'t create more players than there are controls for')
            
        for i in range(count):
            player = Player(i + 1, self.scores[i + 1], controls[i], coords[i], self.shots, self.walls, self.players, self.all_sprites)
            self.player_colors[player.identity] = player.get_sprite_color()

    def last_player_standing(self):
        if len(self.players) == 0: # if all players killed at the same frame
            return 0
        if len(self.players) == 1:
            return self.players.sprites()[0]
        
        return None
    
    def draw_scoreboard(self):
        margins = 200
        start_pos = 50

        for i, (color_k, score_k) in enumerate(zip(self.player_colors.keys(), self.scores.keys())):
            text = self.font.render(f'Score: {self.scores[score_k]}', 1, self.player_colors[color_k])
            x_position = (pg.Surface.get_width(text) + margins) * i + start_pos
            self.screen.blit(text, (x_position, start_pos))
