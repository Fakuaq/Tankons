from config import layouts
from random import randint, shuffle
from wall import Wall
import pygame as pg


class LayoutController:
    """
    A class responsible for managing game layouts, including walls, spawn zones, and powerup zones.

    Attributes:
        - walls (list): A list to store Wall objects representing the layout walls.
        - spawns (list): A list to store Rect objects representing player spawn zones.
        - powerup_zones (list): A list to store Rect objects representing powerup spawn zones.
        - screen (pygame.Surface): The game screen surface.

    Methods:
        - __init__(self, screen, *groups):
            Initializes the LayoutController object with the specified parameters.

        - generate_layout(self):
            Generates a random layout, creating walls, spawn zones, and powerup zones based on a predefined set of layouts.

        - spawn_coordinates(self, player_count):
            Generates random coordinates for player spawns based on the layout's spawn zones.

        - draw_spawn_areas(self):
            Draws rectangles on the screen to visualize player spawn zones.

        - draw_powerup_areas(self):
            Draws rectangles on the screen to visualize powerup spawn zones.

        - powerup_coordinates(self, powerups):
            Generates random coordinates for powerup spawns based on the layout's powerup zones, avoiding overlaps with existing powerups.
    """
    walls = []
    spawns = []
    powerup_zones = []
    _current_layout = None
    
    def __init__(self, screen, *groups):
        """
        Initializes the LayoutController object with the specified parameters.

        Parameters:
            - screen: The pygame screen on which the game is displayed.
            - *groups: Sprite groups to which the LayoutController should belong.

        Returns:
            None
        """
        self.screen = screen
        self.groups = groups

    def pick_layout(self) -> int:
        return randint(0, len(layouts) - 1)

    def render_layout(self, layout_index: int) -> None:
        """
        Generates a random layout for the game.

        Parameters:
            None

        Returns:
            None
        """
        self.spawns = []
        self.powerup_zones = []
        self._current_layout = layout_index
        layout = layouts[layout_index]

        for i in range(len(layout['wall_positions'])):
            self.walls.append(Wall(layout['wall_positions'][i], layout['wall_sizes'][i], *self.groups))

        for i in range(len(layout['spawn_zones'])):
            self.spawns.append(pg.Rect(layout['spawn_zones'][i]))

        for i in range(len(layout['powerup_zones'])):
            self.powerup_zones.append(pg.Rect(layout['powerup_zones'][i]))
        
    def current_layout(self):
        return self._current_layout

    def spawn_coordinates(self, player_count):
        """
        Generates random spawn coordinates for players.

        Parameters:
            - player_count (int): The number of players.

        Returns:
            list: A list of (x, y) coordinates for each player.
        Raises:
            ValueError: If player_count is greater than the number of available spawn positions.
            RuntimeError: If the layout is uninitialized.
        """
        if not self.walls:
            raise RuntimeError('Can\'t call method with uninitialized layout')
        
        if player_count > len(self.spawns):
            raise ValueError('Player count can\'t be bigger than the spawn position count')

        coords = []
        picked_indexes = [] 
        for _ in range(player_count):
            spawn_index = randint(0, len(self.spawns) - 1)
            
            while spawn_index in picked_indexes:
                spawn_index = randint(0, len(self.spawns) - 1)
            
            rect = self.spawns[spawn_index]
            picked_indexes.append(spawn_index)

            x_range = rect.x + rect.width
            y_range = rect.y + rect.height
            x_pos = randint(rect.x, x_range)
            y_pos = randint(rect.y, y_range)

            coords.append((x_pos, y_pos))

        return coords
    
    def draw_spawn_areas(self):
        """
        Draws rectangles representing spawn areas on the screen.

        Parameters:
            None

        Returns:
            None
        """
        for rect in self.spawns:
            pg.draw.rect(self.screen, (255, 255, 122), rect)

    def draw_powerup_areas(self):
        """
        Draws rectangles representing powerup areas on the screen.

        Parameters:
            None

        Returns:
            None
        """
        for rect in self.powerup_zones:
            pg.draw.rect(self.screen, (63, 112, 77), rect)

    def powerup_coordinates(self, powerups):
        """
        Generates random coordinates for powerups within designated powerup zones.

        Parameters:
            - powerups (list): A list of existing powerups to check for collisions.

        Returns:
            tuple or None: Returns a tuple (x_pos, y_pos) representing the random coordinates for a powerup
            or None if all powerup zones are occupied.
        """
        if len(powerups) >= len(self.powerup_zones): return

        zone_without_powerup = False
        shuffle(self.powerup_zones)
        
        for zone in self.powerup_zones:
            if not len(powerups):
                zone_without_powerup = True
            
            for powerup in powerups:
                if powerup.rect.colliderect(zone):
                    zone_without_powerup = False
                    break
                else:
                    zone_without_powerup = True

            if zone_without_powerup:
                x_range = zone.x + zone.width
                y_range = zone.y + zone.height
                x_pos = randint(zone.x, x_range)    
                y_pos = randint(zone.y, y_range)
    
                return x_pos, y_pos
