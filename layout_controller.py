from config import layouts
from random import randint, shuffle
from wall import Wall
import pygame as pg


class LayoutController:
    walls = []
    spawns = []
    powerup_zones = []
    
    def __init__(self, screen, *groups):
        self.screen = screen
        self.groups = groups

    def generate_layout(self):
        self.spawns = []
        self.powerup_zones = []
        
        layout_index = randint(0, len(layouts) - 1)
        layout = layouts[layout_index]

        for i in range(len(layout['wall_positions'])):
            self.walls.append(Wall(layout['wall_positions'][i], layout['wall_sizes'][i], *self.groups))

        for i in range(len(layout['spawn_zones'])):
            self.spawns.append(pg.Rect(layout['spawn_zones'][i]))

        for i in range(len(layout['powerup_zones'])):
            self.powerup_zones.append(pg.Rect(layout['powerup_zones'][i]))

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
    
    def draw_spawn_areas(self):
        for rect in self.spawns:
            pg.draw.rect(self.screen, (255, 255, 122), rect)

    def draw_powerup_areas(self):
        for rect in self.powerup_zones:
            pg.draw.rect(self.screen, (63, 112, 77), rect)

    def powerup_coordinates(self, powerups):
        if len(powerups) >= len(self.powerup_zones): return

        zone_without_powerup = False
        shuffle(self.powerup_zones)
        
        for zone in self.powerup_zones:
            if not len(powerups):
                zone_without_powerup = True
            
            for powerup in powerups:
                if not powerup.rect.colliderect(zone):
                    zone_without_powerup = True

            if zone_without_powerup:
                x_range = zone.x + zone.width
                y_range = zone.y + zone.height
                x_pos = randint(zone.x, x_range)    
                y_pos = randint(zone.y, y_range)
    
                return x_pos, y_pos
