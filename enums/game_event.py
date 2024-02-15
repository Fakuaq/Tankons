from enum import Enum


class GameEvent(Enum):
    JOIN = 'join'
    START_ROUND = 'start_round'
    RESET_ROUND = 'reset_round'
    COORDS = 'coords'
    SHOT = 'shot'
    POWERUP = 'powerup'
