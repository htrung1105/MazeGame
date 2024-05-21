import pygame, sys, re

from maze_generator import Maze
from level import Level
from main import FPS
from settings import *

class Game:
    def __init__(self, screen, maze, TILESIZE):

        # general setup
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.display_surface = pygame.surface.Surface((1300, 700))
        self.level = Level(self.display_surface, maze, TILESIZE)

    def run(self):
        running = True
        img_bg = pygame.image.load("assets/tilemap/ground.png")

        while running:
            # setup display
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.level.getHint()
            self.level.run()

            self.screen.fill('white')
            self.screen.blit(img_bg, (0, 40))
            self.screen.blit(self.display_surface, (0, 40))

            pygame.display.update()
            self.clock.tick(FPS)
