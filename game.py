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
        self.menu = Display(self.screen, {'home' : (815, 589), 'new' : (938, 589), 'save' : (1061, 589), 'help' : (1184, 589)},
                            [('Name: Sheet1', (860, 300)), ('Difficult: Easy', (860, 360)), ('Mode: Auto', (860, 420)), ('Time: 00:00', (860, 480))])

    def run(self):
        running = True
        while running:
            self.display_surface.blit(self.img_ground, (0, 0))
            self.level.run()

            self.screen.blit(self.img_bg, (0, 0))
            self.screen.blit(self.display_surface, (40, 35))
            self.screen.blit(self.img_border, (0, 0))

            status = self.menu.render()
            if status == 'home':
                running = False
            elif status == 'new':
                self.maze.reset()
                self.maze.mazeGenerate()
                self.level = Level(self, int(self.maze.width - 2 * self.maze.wall_width))
                self.menu.reset_time()
            elif status == 'save':
                print('saved')
            elif status == 'help':
                print('help')

            # setup display
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.level.player.getHint()


            pygame.display.update()
            self.clock.tick(FPS)
