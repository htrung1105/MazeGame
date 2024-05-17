import pygame, sys, math
from maze_generator import *

from scripts.entities import PhysicsEntity
from scripts.utils import load_image

class Game:
    def __init__(self, screen, fps, maze):
        # Thông số screen
        pygame.init()
        self.screen, self.fps = screen, fps
        self.clock = pygame.time.Clock()

        self.maze = maze
        self.pos_maze = (41, 32)
        self.movement = [False, False, False, False]

        width, height = screen.get_width(), screen.get_height()
        self.assets = {
            'player': load_image('tom/1.png', 0.8, maze.cell_size, maze.cell_size),
            'goal': load_image('jerry/1.png', 0.8, maze.cell_size, maze.cell_size),
            'background_1':  load_image('background/1.png', 1, width, height),
            'background_2': load_image('background/2.png', 1, width, height),
        }

        self.player = PhysicsEntity(self, 'player', (self.maze.startX, self.maze.startY), (8, 15), 1)
        self.goal = PhysicsEntity(self, 'goal', (self.maze.endX, self.maze.endY), (8, 15), None)

    def run(self):
        running = True
        while running:
            # Lấy vị trí con trỏ
            MOUSE_POS = pygame.mouse.get_pos()
            self.maze.display.fill((255, 255, 255))

            # Cập nhật vị trí player
            self.player.update((self.movement[1] - self.movement[0], self.movement[3] - self.movement[2]),0.2)
            self.player.render(self.maze.display)
            self.goal.render(self.maze.display)

            self.screen.blit(self.assets['background_1'], (0, 0))
            self.maze.render(self.screen, self.pos_maze)
            self.screen.blit(self.assets['background_2'], (0, 0))

            # Lấy thông tin Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False

            # Ngừng trò chơi
            if list(map(int, self.player.pos)) == self.goal.pos:
                running = False

            # Cập nhật display
            pygame.display.update()
            self.clock.tick(self.fps)

SCREEN, FPS = pygame.display.set_mode((1300, 750)), 60
maze = Maze(10, 0, 0, 9, 9, 71)
maze.mazeGenerate()
Game(SCREEN, FPS, maze).run()
