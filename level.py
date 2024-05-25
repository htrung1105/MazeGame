import pygame
from tile import *
from player import Player
from queue import Queue
from maze_solver import MazeSolver
pygame.init()

LIST_DIR_OPPOSITE = [('left', 'right'), ('up', 'down'), ('down', 'up'), ('right', 'left')]

class Level:
    def __init__(self, game, tilesize):

        # get the display surface
        self.display_surface = game.display_surface
        self.game = game

        self.tilesize = tilesize
        self.player = Player(self, game.maze, tilesize)
        self.goal = Goal(self.tilesize, game.maze.grid[game.maze.endX][game.maze.endY])
        self.solver = MazeSolver(game.maze)

        self.stack = []
        self.q = Queue()

        self.visited = []
        self.step = []
        self.stay = []
        self.find = []
        self.index = 0

        self.image_win = pygame.image.load('assets/tilemap/winning.png')
        self.image_win = pygame.transform.scale(self.image_win, (540, 300))

    def getAuto(self, option):
        self.visited.clear()
        self.step = []
        self.stay = []
        self.find = []
        self.index = 0

        if option == 'A*':
            self.visited = self.solver.AStarSearch()
        elif option == 'BFS':
            self.visited = self.solver.BFS()
        self.visited.reverse()

    def run(self):
        self.game.maze.render()
        xx, yy = self.player.loc

        if len(self.visited) > 0:
            x, y, neibor = self.visited.pop()
            self.step.append(Auto('check', self.tilesize, self.game.maze.grid[x][y]))
            if (x, y) in self.stay:
                self.stay.remove((x, y))

            for x, y in neibor:
                self.stay.append(Auto('stay', self.tilesize, self.game.maze.grid[x][y]))

            for icon in self.stay:
                icon.render()

            for icon in self.step:
                icon.render()

            if len(self.visited) == 0:
                tracePath = self.solver.tracePath()
                self.player.hintPath = tracePath
                for x, y in tracePath:
                    self.find.append(Auto('find', self.tilesize, self.game.maze.grid[x][y]))
                    self.find[-1].render()

        else:
            for icon in self.stay:
                icon.render()

            for icon in self.step:
                icon.render()

            for i in range(self.index):
                self.find[i].render()

            if self.index < len(self.find):
                self.index += 1
            else:
                for hint in self.stack:
                    hint.render()

                if self.q.empty():
                    dir = self.player.update(False)
                    if dir in ('left', 'right', 'up', 'down'):
                        self.game.step += 1
                        if len(self.stack) > 0 and (dir, self.stack[-1].dir) in LIST_DIR_OPPOSITE:
                            self.stack.pop()
                        else:
                            self.stack.append(Hint(dir, self.tilesize - 1, self.game.maze.grid[xx][yy]))
                else:
                    self.player.update(True)
                    rect = self.player.image.get_rect(center=self.q.get())
                    self.display_surface.blit(self.player.image, rect)

        if xx == self.game.maze.endX and yy == self.game.maze.endY:
            self.player.status = 'catch'
            rect = self.image_win.get_rect(center = (344, 344))
            self.display_surface.blit(self.image_win, rect)
        else:
            self.goal.render()


