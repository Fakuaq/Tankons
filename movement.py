import pygame as pg

class Movement:
    def __init__(self, coords: tuple, speed: int):
        self._vector = pg.math.Vector2(coords[0], coords[1])
        self.speed = speed

    def move(self, direction_v: pg.math.Vector2):
        result_v = pg.math.Vector2()

        if direction_v.x != 0 or direction_v.y != 0:
            result_v = direction_v.normalize() * self.speed

        self._vector += result_v
        return self._vector
    
    def reset_move(self, coords: pg.math.Vector2):
        self._vector = coords
        
        return self._vector
        