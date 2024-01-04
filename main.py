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
        self.player_array = []

        self.layout_controller = LayoutController(self.walls, self.all_sprites)
        self.layout_controller.generate_layout()
        player_count = len(controls)
        coords = self.layout_controller.spawn_coordinates(player_count)
        
        for i, control_set in enumerate(controls):
            player = Player(i + 1, control_set, (coords[i]), self.shots, self.walls, self.player_array, self.all_sprites)
            self.player_array.append(player)

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
        for player in self.player_array:
            score_text = player.score_text
            if player.identity == 2:
                self.screen.blit(score_text, (50,50))
            else:
                self.screen.blit(score_text, (550 - pg.Surface.get_width(score_text), 50))
    
    def debug_draw(self):
        for rect in self.layout_controller.spawns:
            pygame.draw.rect(self.screen, (255, 255, 122), rect)
    
if __name__ == '__main__':
    game = Game()
    game.run()
