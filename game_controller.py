import pygame as pg
from config import config
from player import Player
from layout_controller import LayoutController
from player_controller import PlayerController
from powerups.powerup_controller import PowerupController
from enums.game_event import GameEvent
from networking.server import Server
from networking.client import Client
from typing import List
from powerups.speed import Speed
from powerups.firerate import FireRate
from powerups.rapid_shot import RapidShot
from powerups.arrow_shot import ArrowShot
from observers.game_event_observable import GameEventObservable
import sys


class GameController:
    _identity = None
    client = None
    server = None
    player_count = 2
    session_started = False
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
        self.player_controller = PlayerController(self.screen, self.scores, self.walls, self.shots, self.players,
                                                  self.all_sprites)
        self.powerup_controller = PowerupController(self.powerups, self.players, self.walls, self.all_sprites)

        if len(sys.argv) > 1 and sys.argv[1] == 'client':
            self.client = Client(self)
            self.client.transmit(GameEvent.JOIN)
        elif len(sys.argv) > 1 and sys.argv[1] == 'server':
            self.server = Server(self)
        else:
            layout = self.layout_controller.pick_layout()
            self.layout_controller.render_layout(layout)
            coords = self.layout_controller.spawn_coordinates(2)
            self.start_game(coords)

    def start_game(self, coords: List[tuple]):
        same_controls = False
        if self.client or self.server:
            same_controls = True

        self.player_controller.spawn_players(self.player_count, coords, self._identity, same_controls)

    def update(self):
        if (self.client or self.server) and not self.session_started: return

        if self.client:
            self.transmit_player_coords()

        self.screen.fill('white')
        self.all_sprites.draw(self.screen)
        self.all_sprites.update()
        self.player_controller.draw_scoreboard()

        self.game_reset_time -= 1
        self.curr_powerup_stat_cd -= 1

        if self.curr_powerup_stat_cd < 0:
            self.curr_powerup_stat_cd = self.powerup_stat_cd
            coords = self.layout_controller.powerup_coordinates(self.powerups)

            powerup_class = powerup = None
            if coords:
                powerup, powerup_class = self.powerup_controller.spawn_powerup(coords)
            if coords and self.server:
                self.server.broadcast(GameEvent.POWERUP, (powerup_class.__name__, powerup.rect.center))

        if not self.game_resetting and not self.client:
            self.check_winner()

        if self.game_resetting and self.game_reset_time < 0:
            self.game_resetting = False
            self.reset_game()

        if config['debug']:
            self.layout_controller.draw_spawn_areas()
            self.layout_controller.draw_powerup_areas()

    def check_winner(self):
        last_player = self.player_controller.last_player_standing()

        if last_player == 0 or isinstance(last_player, Player):
            self.game_resetting = True
            self.game_reset_time = self.game_reset_cd
            if last_player != 0:
                GameEventObservable().set_game_event((GameEvent.RESET_ROUND, last_player.identity))
            else:
                GameEventObservable().set_game_event((GameEvent.RESET_ROUND, last_player))
        if isinstance(last_player, Player):
            self.scores[last_player.identity] += 1

    def reset_game(self):
        for sprite in self.all_sprites:
            sprite.kill()

        if self.server:
            GameEventObservable().set_game_event((GameEvent.START_ROUND, None))
        if not self.server and not self.client:
            layout = self.layout_controller.pick_layout()
            self.layout_controller.render_layout(layout)
            coords = self.layout_controller.spawn_coordinates(2)
            self.start_game(coords)

    def spawn_powerup(self, powerup_class_name, coords):
        _class = globals()[powerup_class_name]

        self.powerup_controller.instantiate_powerup(_class, coords)

    def transmit_player_coords(self):
        coords = self.player_controller.player_coords(self._identity)

        if coords:
            self.client.transmit(GameEvent.COORDS, coords)

    def add_stat_powerup(self, identity, powerup_name):
        self.player_controller.add_stat_powerup(identity, powerup_name)

    def add_shot_powerup(self, identity, powerup):
        self.player_controller.add_shot_powerup(identity, powerup)

    def players_coords(self) -> dict:
        return self.player_controller.players_coords()

    def set_player_coords(self, coords: dict) -> None:
        if self._identity in coords and coords[self._identity]:
            del coords[self._identity]

        return self.player_controller.set_player_coords(coords)

    def player_shoot(self, identity):
        self.player_controller.player_shoot(identity)

    def set_identity(self, value: int):
        self._identity = value

    def pick_layout(self) -> int:
        return self.layout_controller.pick_layout()

    def render_layout(self, layout_index: int):
        self.layout_controller.render_layout(layout_index)

    def spawn_coordinates(self) -> List[tuple]:
        return self.layout_controller.spawn_coordinates(self.player_count)

    def update_scoreboard(self, identity):
        if identity != 0:
            self.player_controller.update_scoreboard(identity)
