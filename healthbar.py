import pygame as pg

class HealthBar(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((206, 26))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(topleft=(20, 20))
        self.health_bar = pg.Surface((200, 20))
        self.health_bar.fill((255, 0, 0))
        self.health_rect = self.health_bar.get_rect(topleft=(self.rect.topleft[0] + 3, self.rect.topleft[1] + 3))
        self.max_health_width = self.health_rect.size[0]

    def update(self):
        screen = pg.display.get_surface()
        screen.blit(self.health_bar, self.health_rect)

    def decrease(self, percent):
        w, h = self.health_bar.get_size()
        if w - (self.max_health_width * percent) >= 0:
            self.health_bar = pg.transform.scale(self.health_bar, (w - (self.max_health_width * percent), h))
