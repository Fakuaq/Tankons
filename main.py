from game_controller import GameController
import pygame as pg


class Game:
    """
        Main class for managing the game loop and initializing the game controller.

        Attributes:
            - clock (pygame.time.Clock): The clock object to control the frame rate.
            - game_controller (GameController): The controller managing the game logic.

        Methods:
            - __init__(self): Initializes the Game object and sets up the game window.
            - run(self): Main game loop to handle events, update the game, and manage the frame rate.
        """
    def __init__(self):
        """
        Initializes the Game object and sets up the game window.
        """
        pg.init()
        pg.display.set_caption('Tankons')
        logo = pg.image.load('assets/tank_1.png')
        pg.display.set_icon(logo)
        screen = pg.display.set_mode((1400, 700))
        
        self.clock = pg.time.Clock()
        self.game_controller = GameController(screen)

        self.run()
    
    def run(self):
        """
        Main game loop to handle events, update the game, and manage the frame rate.
        """
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
