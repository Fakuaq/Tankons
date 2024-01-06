import pygame as pg
import random


class Sounds:

    def death_sound(self):
        type = random.randint(1,4)
        match type:
            case 1:
                sound = pg.mixer.Sound("sounds/Die1.wav")
                pg.mixer.Sound.play(sound)
            case 2:
                sound = pg.mixer.Sound("sounds/Die2.wav")
                pg.mixer.Sound.play(sound)
            case 3:
                sound = pg.mixer.Sound("sounds/Die3.wav")
                pg.mixer.Sound.play(sound)
            case 4:
                sound = pg.mixer.Sound("sounds/Die4.wav")
                pg.mixer.Sound.play(sound)

    def shoot_sound(self):
        type = random.randint(1,3)
        match type:
            case 1:
                sound = pg.mixer.Sound("sounds/Shoot1.wav")
                pg.mixer.Sound.play(sound)
            case 2:
                sound = pg.mixer.Sound("sounds/Shoot2.wav")
                pg.mixer.Sound.play(sound)
            case 3:
                sound = pg.mixer.Sound("sounds/Shoot3.wav")
                pg.mixer.Sound.play(sound)
            case 4:
                sound = pg.mixer.Sound("sounds/Shoot4.wav")
                pg.mixer.Sound.play(sound)

    def powerup_sound(self):
        type = random.randint(1,3)
        match type:
            case 1:
                sound = pg.mixer.Sound("sounds/Powerup1.wav")
                pg.mixer.Sound.play(sound)
            case 2:
                sound = pg.mixer.Sound("sounds/Powerup2.wav")
                pg.mixer.Sound.play(sound)
            case 3:
                sound = pg.mixer.Sound("sounds/Powerup3.wav")
                pg.mixer.Sound.play(sound)