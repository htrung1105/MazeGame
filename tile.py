import pygame

class Goal(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('assets/test/goal.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (setting.tilesize, setting.tilesize))
        self.rect = self.image.get_rect(topleft = pos)

class Hint(pygame.sprite.Sprite):
    def __init__(self, pos, dir, groups):
        super().__init__(groups)
        self.pos = pos
        self.image = pygame.image.load(rf'assets/test/hint_{dir}.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (setting.tilesize, setting.tilesize))
        self.rect = self.image.get_rect(topleft = pos)