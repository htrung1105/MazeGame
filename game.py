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

        self.img_ground = pygame.image.load('assets/tilemap/ground.png')
        self.img_bg = pygame.image.load('assets/tilemap/background.png')
        self.img_border = pygame.image.load('assets/tilemap/border.png')
        self.display_surface = maze.screen

        self.maze = maze
        self.level = Level(self, int(maze.width - 2 * maze.wall_width))
        #self.menu = Display(self.screen)

    def run(self):
        running = True
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
                        pass
                       # self.menu.run()

            self.display_surface.blit(self.img_ground, (0, 0))
            self.level.run()

            self.screen.blit(self.img_bg, (0, 0))
            self.screen.blit(self.display_surface, (40, 35))
            self.screen.blit(self.img_border, (0, 0))

            pygame.display.update()
            self.clock.tick(FPS)
