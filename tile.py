import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('assets/test/rock.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)

class Goal(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('assets/test/goal.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)