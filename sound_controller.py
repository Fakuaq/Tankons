import pygame as pg
import random


class SoundController:
    """
    A class for managing game sounds.

    Class Methods:
        - death_sound(): Play a random death sound.
        - shoot_sound(): Play a random shoot sound.
        - powerup_sound(): Play a random powerup sound.
        - powerup_bigshot_sound(): Play a big shot powerup sound.
        - powerup_arrowshot_sound(): Play an arrow shot powerup sound.
    """
    
    @classmethod
    def death_sound(cls):
        """
        Play a random death sound.
        """
        sound_type = random.randint(1,4)
        match sound_type:
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

    @classmethod
    def shoot_sound(cls):
        """
        Play a random shoot sound.
        """
        sound_type = random.randint(1,3)
        match sound_type:
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

    @classmethod
    def powerup_sound(cls):
        """
        Play a random powerup sound.
        """
        sound_type = random.randint(1,3)
        match sound_type:
            case 1:
                sound = pg.mixer.Sound("sounds/Powerup1.wav")
                pg.mixer.Sound.play(sound)
            case 2:
                sound = pg.mixer.Sound("sounds/Powerup2.wav")
                pg.mixer.Sound.play(sound)
            case 3:
                sound = pg.mixer.Sound("sounds/Powerup3.wav")
                pg.mixer.Sound.play(sound)

    @classmethod
    def powerup_bigshot_sound(cls):
        """
        Play a big shot powerup sound.
        """
        sound = pg.mixer.Sound("sounds/Bigshot.wav")
        pg.mixer.Sound.play(sound)

    @classmethod
    def powerup_arrowshot_sound(cls):
        """
        Play an arrow shot powerup sound.
        """
        sound = pg.mixer.Sound("sounds/ArrowShot.wav")
        pg.mixer.Sound.play(sound)
