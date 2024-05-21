import pygame, sys

from maze_generator import Maze
from level import Level
from settings import setting

class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = setting.screen
        self.clock = pygame.time.Clock()

        setting.tilesize = 64
        self.level = Level()

    def run(self):
        running = True
        img_bg = pygame.image.load('assets/tilemap/ground.png')

        while running:
            # setup display
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        pass
                        #self.level.getHint()

            self.screen.blit(img_bg, (0, 0))
            self.level.run()

            pygame.display.update()
            self.clock.tick(setting.fps)
