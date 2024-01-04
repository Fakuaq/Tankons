import pygame as pg

config = {
    'debug': 0
}

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
        'wall_sizes': [(1000, 10), (1000, 10), (10, 510), (10, 510), (10, 300), (400, 10), (10, 160)],
        'wall_positions': [(200, 100), (200, 600), (200, 100), (1200, 100), (500, 100), (500, 300), (800, 440)],
        'spawn_zones': [(230, 130, 100, 100), (1080, 480, 20, 20), (1080, 130, 100, 100)],
    },
]