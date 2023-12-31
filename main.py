from player import *
from god import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((600, 600))
        self.background = pg.transform.scale(pg.image.load('assets/bg.png'), self.screen.get_size())
        self.clock = pg.time.Clock()

        self.all_sprites = pg.sprite.Group()
        self.enemy_shots = pg.sprite.Group()
        self.player_shots = pg.sprite.Group()
        self.player = Player((100, 100), self.player_shots, self.enemy_shots, self.all_sprites)
        self.god = God((400, 400), self.player_shots, self.enemy_shots, self.all_sprites)
        
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
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.all_sprites.update()
            
if __name__ == '__main__':
    game = Game()
    game.run()
