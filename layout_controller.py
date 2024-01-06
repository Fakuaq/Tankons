from config import layouts
from random import randint
from wall import Wall
import pygame as pg


class LayoutController:
    walls = []
    spawns = []
    
    def __init__(self, *groups):
        self.groups = groups

    def generate_layout(self):
        self.spawns = []
        
        layout_index = randint(0, len(layouts) - 1)
        layout = layouts[layout_index]

        for i in range(len(layout['wall_positions'])):
            self.walls.append(Wall(layout['wall_positions'][i], layout['wall_sizes'][i], *self.groups))

        for i in range(len(layout['spawn_zones'])):
            self.spawns.append(pg.Rect(layout['spawn_zones'][i]))

    def spawn_coordinates(self, player_count):
        if player_count > len(self.spawns):
            raise ValueError('Player count can\'t be bigger than the spawn position count')

        if not self.walls:
            raise RuntimeError('Can\'t call method with uninitialized layout')

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
