import pygame
from tile import *
from player import Player
pygame.init()

LIST_DIR_OPPOSITE = [('left', 'right'), ('up', 'down'), ('down', 'up'), ('right', 'left')]

class Level:
    def __init__(self, game, tilesize):

        # get the display surface
        self.display_surface = game.display_surface
        self.width, self.height = self.display_surface.get_size()
        self.game = game

        self.tilesize = tilesize
        self.player = Player(game.maze, tilesize)
        self.goal = Goal(self.tilesize, game.maze.grid[game.maze.endX][game.maze.endY])
        self.stack = []

    def run(self):
        self.game.maze.render()
        x, y = self.player.loc

        if x == self.game.maze.endX and y == self.game.maze.endY:
            self.player.status = 'catch'
        else:
            self.goal.render()

        dir = self.player.update()
        if dir in ('left', 'right', 'up', 'down'):
            if len(self.stack) > 0 and (dir, self.stack[-1].dir) in LIST_DIR_OPPOSITE:
                self.stack.pop()
            else:
                self.stack.append(Hint(dir, self.tilesize, self.game.maze.grid[x][y]))

        for hint in self.stack:
            hint.render()

        # # winning
        # if self.pause is False and self.goal.rect.colliderect(self.player.rect):
        #     self.player.rect = self.goal.rect
        #     self.player.pause = True
        #     self.pause = True
        #     self.visible_sprites.remove(self.goal)
        #
        # # save old pos of player
        # pre_pos = self.player.rect.topleft
        #
        # # update and draw the game
        # self.visible_sprites.custom_draw(self.player, self.num_row, self.num_col)
        # self.visible_sprites.update()
        #
        # # get new pos of player
        # now_pos = self.player.rect.topleft
        # dx, dy = now_pos[0] - pre_pos[0], now_pos[1] - pre_pos[1]
        #
        # if dx != 0 or dy != 0:
        #     if dx > 0:
        #         status = 'right'
        #     elif dx < 0:
        #         status = 'left'
        #     elif dy > 0:
        #         status = 'down'
        #     else:
        #         status = 'up'
        #
        #     if len(self.stack) > 0 and now_pos == self.stack[-1].pos:
        #         self.visible_sprites.remove(self.stack.pop())
        #     else:
        #         self.stack.append(Hint(pre_pos, status, [self.visible_sprites]))
        #
        # # return game is running or not
        # return self.pause