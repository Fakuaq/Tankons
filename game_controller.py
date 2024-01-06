import pygame as pg
from config import config
from player import Player
from layout_controller import LayoutController
from player_controller import PlayerController


class GameController:
    player_count = 2
    game_resetting = False
    game_reset_cd = 60
    game_reset_time = game_reset_cd
    
    def __init__(self, screen):
        self.screen = screen
        self.scores = {}
        for i in range(self.player_count):
            self.scores[i + 1] = 0

        self.all_sprites = pg.sprite.Group()
        self.shots = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.players = pg.sprite.Group()

        self.layout_controller = LayoutController(self.walls, self.all_sprites)
        self.player_controller = PlayerController(self.scores, self.walls, self.shots, self.players, self.all_sprites)

        self.start_game()

    def start_game(self):
        self.layout_controller.generate_layout()
        coords = self.layout_controller.spawn_coordinates(self.player_count)
        self.player_controller.spawn_players(self.player_count, coords)

    def update(self):
        self.screen.fill('white')
        self.draw_player_score()
        self.all_sprites.draw(self.screen)
        self.all_sprites.update()
        self.game_reset_time -= 1

        if not self.game_resetting:
            self.check_winner()
    
        if self.game_resetting and self.game_reset_time < 0:
            self.game_resetting = False
            self.reset_game()

        if config['debug']:
            self.debug_draw()

    def check_winner(self):
        last_player = self.player_controller.last_player_standing()

        if last_player == 0:  # game is a draw
            self.game_resetting = True
            self.game_reset_time = self.game_reset_cd
        elif isinstance(last_player, Player):
            self.scores[last_player.identity] += 1
            self.game_resetting = True
            self.game_reset_time = self.game_reset_cd

    def reset_game(self):
        for sprite in self.all_sprites:
            sprite.kill()

        self.start_game()

    def draw_player_score(self):
        margins = 200
        start_pos = 50

        for i, player in enumerate(self.players):
            x_position = (pg.Surface.get_width(player.score_text) + margins) * i + start_pos
            self.screen.blit(player.score_text, (x_position, start_pos))

    def debug_draw(self):
        for rect in self.layout_controller.spawns:
            pg.draw.rect(self.screen, (255, 255, 122), rect)
