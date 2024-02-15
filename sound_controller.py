import pygame as pg
import random


class SoundController:
    base_path = 'assets/sounds/'

    @classmethod
    def death_sound(cls):
        sound_type = random.randint(1, 4)
        pg.mixer.Sound.play(pg.mixer.Sound(f'{cls.base_path}Die{sound_type}.wav'))

    @classmethod
    def shoot_sound(cls):
        sound_type = random.randint(1, 3)
        pg.mixer.Sound.play(pg.mixer.Sound(f'{cls.base_path}Shoot{sound_type}.wav'))

    @classmethod
    def powerup_sound(cls):
        sound_type = random.randint(1, 3)
        pg.mixer.Sound.play(pg.mixer.Sound(f'{cls.base_path}Powerup{sound_type}.wav'))

    @classmethod
    def powerup_bigshot_sound(cls):
        sound = pg.mixer.Sound(f'{cls.base_path}BigShot.wav')
        pg.mixer.Sound.play(sound)

    @classmethod
    def powerup_arrowshot_sound(cls):
        sound = pg.mixer.Sound(f'{cls.base_path}ArrowShot.wav')
        pg.mixer.Sound.play(sound)
