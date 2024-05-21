import pygame

from game import *
from maze_solver import *
from maze_generator import *

import pickle # save game/load game library

# constant
WIDTH, HEIGHT, FPS = 1300, 750, 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game by Group 2 - 23TNT1")

# save a maze into a file
def saveMaze(maze: Maze, filename: str):
    with open(filename, 'wb') as f:
        pickle.dump(maze, f)

# load a maze from a file and return it
def loadMaze(filename: str):
    with open(filename, 'rb') as f:
        maze = pickle.load(f)
    return maze

def getImage(filename: str):
    return pygame.image.load(rf'assets\{filename}').convert_alpha()

# main function
def main():
    clock = pygame.time.Clock()
    run = True

    maze = Maze(5, 0, 0, 4, 4)
    maze.mazeGenerate()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        game = Game(SCREEN, maze, 50)
        game.run()

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()