import pygame, sys

from main import FPS
from level import Level
from Display import *

class Game:
    def __init__(self, screen, maze):

        # general setup
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.maze = maze
        self.level = Level(self, int(maze.width - 2 * maze.wall_width))
        self.menu = Display(self.screen)

    def run(self):
        running = True
        img_bg = pygame.image.load('assets/tile/ground.png')

        while running:
            # setup display
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.level.player.getHint()
                    if event.key == pygame.K_ESCAPE:
                        self.menu.run()

            self.screen.blit(img_bg, (0, 0))
            self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)
