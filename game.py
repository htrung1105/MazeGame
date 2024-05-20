import pygame, sys, re

from maze_generator import Maze
from level import Level

class Game:
    def __init__(self, screen, WORLD_MAP, TILESIZE):

        # general setup
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.level = Level(screen, WORLD_MAP, TILESIZE)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            print(self.level.run())

            pygame.display.update()
            self.clock.tick(60) # FPS = 60

if __name__ == '__main__':
    screen = pygame.display.set_mode((1300, 750))
    maze = Maze(5, 0, 0, 4, 4)
    maze.mazeGenerate()
    WORLD_MAP = maze.convert()
    TILESIZE = 64

    game = Game(screen, WORLD_MAP, TILESIZE)
    game.run()
