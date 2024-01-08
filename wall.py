import pygame as pg

class Wall(pg.sprite.Sprite):
    """A class representing a wall in the game.

    This class inherits from pygame's Sprite class and is used to create
    wall objects with a specified position and size.

    Parameters:
    - pos (tuple): The top-left corner position (x, y) of the wall.
    - size (tuple): The size (width, height) of the wall.
    - *groups: Variable length argument list of sprite groups to add the wall to.

    Attributes:
    - image (pygame.Surface): The surface representing the visual appearance of the wall.
    - rect (pygame.Rect): The rectangular area occupied by the wall on the screen.

    Note:
    The wall is initialized with a black color.

    Example:
    wall = Wall((100, 200), (30, 40), all_sprites, walls_group)
    """
    def __init__(self, pos, size, *groups):
        self.image = pg.Surface(size)
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)
        
        super().__init__(*groups)