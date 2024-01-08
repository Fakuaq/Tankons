from config import controls
from player import Player
import pygame as pg
pg.font.init()

class PlayerController:
    """
    A class for managing and controlling player functionality, including spawning, scoring, and scoreboard display.

    Attributes:
        - player_colors (dict): A dictionary mapping player identities to their respective tank colors.
        - font (pygame.font.Font): The font object for rendering text.
        - screen (pygame.Surface): The game screen surface.
        - scores (dict): A dictionary mapping player identities to their scores.
        - walls (pygame.sprite.Group): The group of wall sprites.
        - shots (pygame.sprite.Group): The group of shot sprites.
        - players (pygame.sprite.Group): The group of player sprites.
        - all_sprites (pygame.sprite.Group): The group of all sprites.
        - player_images (list): A list containing images of player tanks.
        
    Methods:
        - __init__(self, screen, scores, walls, shots, players, all_sprites):
            Initializes the PlayerController with the specified parameters.

        - spawn_players(self, count, coords):
            Spawns player objects with the specified count and initial coordinates.

        - last_player_standing(self):
            Checks if only one player is left in the game.

        - draw_scoreboard(self):
            Draws the player scoreboard on the screen.
    """
    player_colors = {}
    font = pg.font.SysFont("San Francisco", 60)
    
    def __init__(self, screen, scores, walls, shots, players, all_sprites):
        self.screen = screen
        self.scores = scores
        self.walls = walls
        self.shots = shots
        self.players = players
        self.all_sprites = all_sprites
        self.player_images = []
        
    def spawn_players(self, count, coords):
        """
        Spawns as much players at the specified coordinates as the count indicates.

        Parameters:
            - count (int): The number of players to spawn.
            - coords (list): A list of tuples containing initial coordinates for each player.

        Returns:
            None
        """
        if count > len(controls):
            raise RuntimeError('Can\'t create more players than there are controls for')
            
        for i in range(count):
            player = Player(i + 1, self.scores[i + 1], controls[i], coords[i], self.shots, self.walls, self.players, self.all_sprites)
            self.player_colors[player.identity] = player.get_sprite_color()
            self.player_images.append(player.image_copy)

    def last_player_standing(self):
        """
        Checks if only one player is left in the game.

        Parameters:
            None

        Returns:
            int or None: If one player is left, returns the identity of that player. Otherwise, returns None.
        """
        if len(self.players) == 0: # if all players killed at the same frame
            return 0
        if len(self.players) == 1:
            return self.players.sprites()[0]
        
        return None

    def draw_scoreboard(self):
        """
        Draws the player scoreboard on the screen.

        Parameters:
            None

        Returns:
            None
        """
        if self.player_images:
            score_x_offset = 50
            tank_y_offset = 7
            scoreboard_x_offset = 100
            margins = 100
            y_axis = 50
            x_axis = self.screen.get_width() / 2 - scoreboard_x_offset
            score_color = (0,0,0)
            
            # Draw each scoreboard element
            for i, (player_identity, score) in enumerate(self.scores.items()):
                tank_image = self.player_images[player_identity - 1]

                x_position = x_axis + (tank_image.get_width() + margins) * i
                y_position = y_axis - tank_image.get_height() / 2 - tank_y_offset
                # Draw tank image
                self.screen.blit(tank_image, (x_position, y_position))

                # Draw score number next to the tank image
                score_text = self.font.render(str(score), 1, score_color)
                score_x = x_position + score_x_offset
                score_y = y_axis - score_text.get_height() / 2
                self.screen.blit(score_text, (score_x, score_y))