from movement import Movement
import pygame as pg
from random import randint

class God(pg.sprite.Sprite, Movement):
    shot_cd = 60
    speed = 1

    def __init__(self, pos, player_shots, enemy_shots, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.screen = pg.display.get_surface()
        self.image = pg.Surface((40, 40))
        self.image.fill((200, 30, 30))
        self.rect = self.image.get_rect(center=pos)

        self.move_dir_timer = 0
        self.move_dir_cd = randint(20, 60)
        self.current_shot_cd = self.shot_cd

        self.direction_v = pg.math.Vector2(0, 0)
        
        self.hp = 40
        
        self.enemy_shots = enemy_shots
        self.player_shots = player_shots

        Movement.__init__(self, self.rect.center, self.speed)

    def update(self):
        # movement updates
        self.move_dir_timer += 1
        if self.move_dir_timer >= self.move_dir_cd:
            self.move_dir_timer = 0
            self.move_dir_cd = randint(20, 60)
            self.direction_v = pg.math.Vector2(randint(-1, 1), randint(-1, 1))

        self.rect.center = self.move(self.direction_v)

        # shot updates
        self.current_shot_cd -= 1
        if self.current_shot_cd <= 0:
            self.shoot()
            self.current_shot_cd = self.shot_cd
            
        # collision detection
        if pg.sprite.spritecollideany(self, self.player_shots):
            shot = pg.sprite.spritecollideany(self, self.player_shots)
            self.hp -= shot.damage
            shot.kill()
            if self.hp <= 0:
                self.kill()
        
    def shoot(self):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    Shot(self.rect.center, pg.math.Vector2(i, j), 20, 2, (200, 30, 30), self.enemy_shots, *self.groups())

class Shot(pg.sprite.Sprite, Movement):
    life_cd = 60 * 3
    
    def __init__(self, position, direction, damage, speed, color, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.current_life_cd = self.life_cd
        self.image = pg.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.direction = direction
        self.damage = damage

        Movement.__init__(self, position, self.speed)

    def update(self):
        self.rect.center = self.move(self.direction)

        self.current_life_cd -= 1

        if self.current_life_cd <= 0:
            self.kill()
