from player import Player
from wall import Wall
from config import controls
import pygame as pg

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((600, 600))
        self.clock = pg.time.Clock()

        self.all_sprites = pg.sprite.Group()
        self.shots = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        
        for i, control_set in enumerate(controls):
            Player(i + 1, control_set,(100 * (i + 1), 100 * (i + 1)), self.shots, self.walls, self.all_sprites)

        # TODO remove these after map rendering is implemented
        Wall((380, 100), (10, 180), self.walls, self.all_sprites)
        Wall((300, 90), (90, 10), self.walls, self.all_sprites)
        
        self.run()
    
    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            self.update()
            self.clock.tick(60)
            pg.display.update()
            
    def update(self):
        self.screen.fill('white')
        self.all_sprites.draw(self.screen)
        self.all_sprites.update()
            
if __name__ == '__main__':
    game = Game()
    game.run()
