import pygame
from tile import *
from player import Player
from queue import Queue
pygame.init()

LIST_DIR_OPPOSITE = [('left', 'right'), ('up', 'down'), ('down', 'up'), ('right', 'left')]

class Level:
    def __init__(self, game, tilesize):

        # get the display surface
        self.display_surface = game.display_surface
        self.width, self.height = self.display_surface.get_size()
        self.game = game

        self.tilesize = tilesize
        self.player = Player(self, game.maze, tilesize)
        self.goal = Goal(self.tilesize, game.maze.grid[game.maze.endX][game.maze.endY])

        self.stack = []
        self.q = Queue()

    def run(self):
        self.game.maze.render()
        x, y = self.player.loc

        if x == self.game.maze.endX and y == self.game.maze.endY:
            self.player.status = 'catch'
        else:
            self.goal.render()

        for hint in self.stack:
            hint.render()

        if self.q.empty():
            dir = self.player.update(False)
            if dir in ('left', 'right', 'up', 'down'):
                self.game.step += 1
                if len(self.stack) > 0 and (dir, self.stack[-1].dir) in LIST_DIR_OPPOSITE:
                    self.stack.pop()
                else:
                    self.stack.append(Hint(dir, self.tilesize - 1, self.game.maze.grid[x][y]))
        else:
            self.player.update(True)
            rect = self.player.image.get_rect(center=self.q.get())
            self.display_surface.blit(self.player.image, rect)

