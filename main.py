from player import Player
import pygame as pg

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((600, 600))
        self.clock = pg.time.Clock()

        self.all_sprites = pg.sprite.Group()
        self.player_shots = pg.sprite.Group()
        self.player = Player((100, 100), self.player_shots, self.all_sprites)
        
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
