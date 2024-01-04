import pygame as pg

controls = [
    {
        'up': pg.K_UP,
        'down': pg.K_DOWN,
        'rotate_left': pg.K_LEFT,
        'rotate_right': pg.K_RIGHT,
        'shoot': pg.K_SLASH
    },
    {
        'up': pg.K_w,
        'down': pg.K_s,
        'rotate_left': pg.K_a,
        'rotate_right': pg.K_d,
        'shoot': pg.K_f
    }
]

layouts = [
    {
        'wall_sizes': [(10, 180), (90, 10)],
        'wall_positions': [(380, 100), (300, 90)],
        'spawns': [(0, 0, 100, 100), (200, 200, 20, 20)],
    },
]