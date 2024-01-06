import pygame.draw
from player import Player
from config import controls, config
from layout_controller import LayoutController
import pygame as pg
pg.font.init()

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1400, 700))
        self.clock = pg.time.Clock()

        self.all_sprites = pg.sprite.Group()
        self.shots = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.players = pg.sprite.Group()

        self.layout_controller = LayoutController(self.walls, self.all_sprites)
        self.layout_controller.generate_layout()
        player_count = len(controls)
        coords = self.layout_controller.spawn_coordinates(player_count)
        
        for i, control_set in enumerate(controls):
            Player(i + 1, control_set, (coords[i]), self.shots, self.walls, self.players, self.all_sprites)

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
        self.draw_player_score()
        self.all_sprites.draw(self.screen)
        self.all_sprites.update()

        if config['debug']:
            self.debug_draw()
    
    def draw_player_score(self):
        margins = 200
        start_pos = 50
        
        for i, player in enumerate(self.players):
            x_position = (pg.Surface.get_width(player.score_text) + margins) * i + start_pos
            self.screen.blit(player.score_text, (x_position, start_pos))
    
    def debug_draw(self):
        for rect in self.layout_controller.spawns:
            pygame.draw.rect(self.screen, (255, 255, 122), rect)
    
if __name__ == '__main__':
    game = Game()
    game.run()
