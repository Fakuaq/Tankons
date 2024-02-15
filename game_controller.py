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
    """
    Class managing the game logic and interactions between game components.

    Attributes:
        - player_count (int): The number of players in the game.
        - game_resetting (bool): Flag indicating whether the game is resetting.
        - game_reset_cd (int): Cooldown in frames for game reset.
        - game_reset_time (int): Current countdown for game reset.
        - powerup_stat_cd (int): Cooldown in frames for player stat powerup update.
        - curr_powerup_stat_cd (int): Current countdown for player stat powerup update.
        - all_sprites (pygame.sprite.Group): Group containing all game sprites.
        - shots (pygame.sprite.Group): Group containing shot sprites.
        - walls (pygame.sprite.Group): Group containing wall sprites.
        - particles (pygame.sprite.Group): Group containing particle sprites.
        - players (pygame.sprite.Group): Group containing player sprites.
        - powerups (pygame.sprite.Group): Group containing powerup sprites.

    Methods:
        - __init__(self, screen): Initializes the GameController object.
        - start_game(self): Initializes the game by generating layout and spawning players.
        - update(self): Updates the game state, handles events, and manages game flow.
        - check_winner(self): Checks if there is a winner and if the game should reset.
        - reset_game(self): Resets the game state for a new round.
    """
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
        """
        Initializes the GameController object.

        Parameters:
            - screen (pygame.Surface): The game screen surface.
        """
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
        self.powerup_controller = PowerupController(self.powerups, self.players, self.walls, self.all_sprites)
        
        if sys.argv[1] == 'client':
            self.client = Client(self)
            self.client.transmit(GameEvent.JOIN)
        elif sys.argv[1] == 'server':
            self.server = Server(self)

    def start_game(self, coords: List[tuple]):
        """
        Starts a new game by generating the layout and spawning players.
        
        Parameters:
            None

        Returns:
            None
        """
        self.player_controller.spawn_players(self.player_count, coords, self._identity, True)

    def update(self):        
        """
        Updates the game state, including drawing sprites, handling game logic, and resetting the game.

        Parameters:
            None

        Returns:
            None
        """
        if not self.session_started: return
        
        if self.client:
            self.transmit_player_coords()
        
        self.screen.fill('white')
        self.all_sprites.draw(self.screen)
        self.all_sprites.update()
        self.player_controller.draw_scoreboard()
        
        self.game_reset_time -= 1
        self.curr_powerup_stat_cd -= 1

        if self.curr_powerup_stat_cd < 0 and self.server:
            self.curr_powerup_stat_cd = self.powerup_stat_cd
            coords = self.layout_controller.powerup_coordinates(self.powerups)
            if coords:
                powerup, powerup_class = self.powerup_controller.spawn_powerup(coords)
                self.server.broadcast(GameEvent.POWERUP, (powerup_class.__name__, powerup.rect.center))

        if not self.game_resetting and self.server:
            self.check_winner()
    
        if self.game_resetting and self.game_reset_time < 0:
            self.game_resetting = False
            self.reset_game()

        if config['debug']:
            self.layout_controller.draw_spawn_areas()
            self.layout_controller.draw_powerup_areas()

    def check_winner(self):
        """
        Checks if there is a winner in the game and triggers a game reset if needed.

        Parameters:
            None

        Returns:
            None
        """
        last_player = self.player_controller.last_player_standing()

        if last_player == 0 or isinstance(last_player, Player):
            self.game_resetting = True
            self.game_reset_time = self.game_reset_cd
            if last_player != 0:
                GameEventObservable().set_game_event(('reset_round', last_player.identity))
            else:
                GameEventObservable().set_game_event(('reset_round', last_player))
        if isinstance(last_player, Player):
            self.scores[last_player.identity] += 1

    def reset_game(self):
        """
        Resets the game by removing all sprites from the screen and starting a new game.

        Parameters:
            None

        Returns:
            None
        """
        for sprite in self.all_sprites:
            sprite.kill()

        if self.server:
            GameEventObservable().set_game_event(('start_round', None))

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
