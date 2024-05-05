import pygame
from maze_generator import *
from maze_solver import *
import pickle # save game/load game library

# constant
WIDTH, HEIGHT = 1300, 750
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# save a maze into a file
def saveMaze(maze: Maze, filename: str):
    with open(filename, 'wb') as f:
        pickle.dump(maze, f)

# load a maze from a file and return it
def loadMaze(filename: str):
    with open(filename, 'rb') as f:
        maze = pickle.load(f)
    return maze

# main function
def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

if __name__ == '__main__':
    main()