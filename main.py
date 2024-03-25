from game_controller import GameController
import pygame as pg


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tankons')
        logo = pg.image.load('assets/players/tank_1.png')
        pg.display.set_icon(logo)
        screen = pg.display.set_mode((1400, 700))
        
        self.clock = pg.time.Clock()
        self.game_controller = GameController(screen)

        self.run()
    
    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            self.game_controller.update()
            self.clock.tick(60)
            pg.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
