import pygame as pg
from config import config
from player import Player
from layout_controller import LayoutController
from player_controller import PlayerController
from powerups.powerup_controller import PowerupController


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
    player_count = 2
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

        self.start_game()

    def start_game(self):
        """
        Starts a new game by generating the layout and spawning players.
        
        Parameters:
            None

        Returns:
            None
        """
        self.layout_controller.generate_layout()
        coords = self.layout_controller.spawn_coordinates(self.player_count)
        self.player_controller.spawn_players(self.player_count, coords)

    def update(self):
        """
        Updates the game state, including drawing sprites, handling game logic, and resetting the game.

        Parameters:
            None

        Returns:
            None
        """
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

        self.start_game()
