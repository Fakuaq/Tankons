from player import Player
from wall import Wall
from config import controls
import pygame as pg
pg.font.init()

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((600, 600))
        self.clock = pg.time.Clock()

        self.all_sprites = pg.sprite.Group()
        self.shots = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.player_array = []
        
        for i, control_set in enumerate(controls):
            player = Player(i + 1, control_set,(100 * (i + 1), 100 * (i + 1)), self.shots, self.walls, self.player_array, self.all_sprites)
            self.player_array.append(player)

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
        self.draw_player_score()
        self.all_sprites.draw(self.screen)
        self.all_sprites.update()
    
    def draw_player_score(self):
        for player in self.player_array:
            score_text = player.score_text
            if player.identity == 2:
                self.screen.blit(score_text, (50,50))
            else:
                self.screen.blit(score_text, (550 - pg.Surface.get_width(score_text), 50))
    
if __name__ == '__main__':
    game = Game()
    game.run()
