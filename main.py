from player import Player
from config import controls
from layout_controller import LayoutController
import pygame as pg

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1400, 700))
        self.clock = pg.time.Clock()

        self.all_sprites = pg.sprite.Group()
        self.shots = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        layout_controller = LayoutController(self.walls, self.all_sprites)
        layout_controller.generate_layout()
        player_count = len(controls)
        coords = layout_controller.spawn_coordinates(player_count)
        
        for i, control_set in enumerate(controls):
            Player(i + 1, control_set, (coords[i]), self.shots, self.walls, self.all_sprites)
        
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
