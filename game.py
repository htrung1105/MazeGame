import pygame, sys

from maze_generator import Maze
from settings import *
from level import Level

class Game:
    def __init__(self, screen, WORLD_MAP):

        # general setup
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.level = Level(WORLD_MAP)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    maze = Maze(40, 0, 0, 39, 39)
    maze.mazeGenerate()
    WORLD_MAP = maze.convert()

    for row in WORLD_MAP:
        print(row)

    game = Game(screen, WORLD_MAP)
    game.run()
