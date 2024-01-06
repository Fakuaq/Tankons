import pygame as pg
from config import config
from player import Player
from layout_controller import LayoutController
from player_controller import PlayerController
from powerups.powerup_controller import PowerupController


class GameController:
    player_count = 2
    game_resetting = False
    game_reset_cd = 60
    game_reset_time = game_reset_cd
    powerup_stat_cd = 60 * 5
    curr_powerup_stat_cd = powerup_stat_cd
    
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
        self.powerups = pg.sprite.Group()

        self.layout_controller = LayoutController(self.screen, self.walls, self.all_sprites)
        self.player_controller = PlayerController(self.screen, self.scores, self.walls, self.shots, self.players, self.all_sprites)
        self.powerup_controller = PowerupController(self.powerups, self.players, self.all_sprites)

        self.start_game()

    def start_game(self):
        self.layout_controller.generate_layout()
        coords = self.layout_controller.spawn_coordinates(self.player_count)
        self.player_controller.spawn_players(self.player_count, coords)

    def update(self):
        self.screen.fill('white')
        self.all_sprites.draw(self.screen)
        self.all_sprites.update()
        self.player_controller.draw_scoreboard()
        
        self.game_reset_time -= 1
        self.curr_powerup_stat_cd -= 1

        if self.curr_powerup_stat_cd < 0:
            self.curr_powerup_stat_cd = self.powerup_stat_cd
            coords = self.layout_controller.powerup_coordinates(self.powerups)
            if coords:
                self.powerup_controller.spawn_powerup(coords)

        if not self.game_resetting:
            self.check_winner()
    
        if self.game_resetting and self.game_reset_time < 0:
            self.game_resetting = False
            self.reset_game()

        if config['debug']:
            self.layout_controller.draw_spawn_areas()

    def check_winner(self):
        last_player = self.player_controller.last_player_standing()

        if last_player == 0 or isinstance(last_player, Player):
            self.game_resetting = True
            self.game_reset_time = self.game_reset_cd
        if isinstance(last_player, Player):
            self.scores[last_player.identity] += 1

    def reset_game(self):
        for sprite in self.all_sprites:
            sprite.kill()

        self.start_game()
