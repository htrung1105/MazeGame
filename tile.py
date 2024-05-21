import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, tilesize, groups):
        super().__init__(groups)
        self.image = pygame.image.load('assets/test/rock.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (tilesize, tilesize))
        self.rect = self.image.get_rect(topleft = pos)

class Goal(pygame.sprite.Sprite):
    def __init__(self, pos, tilesize, groups):
        super().__init__(groups)
        self.image = pygame.image.load('assets/test/goal.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (tilesize, tilesize))
        self.rect = self.image.get_rect(topleft = pos)

class Hint(pygame.sprite.Sprite):
    def __init__(self, pos, tilesize, dir, groups):
        super().__init__(groups)
        self.pos = pos
        self.image = pygame.image.load(rf'assets/test/hint_{dir}.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (tilesize, tilesize))
        self.rect = self.image.get_rect(topleft = pos)