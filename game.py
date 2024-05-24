import pygame, sys

from maze_generator import *
from level import Level
from main import FPS
from Display import *
from database import *

# level: size_map, cell_width, wall_width
ATRIBUTES = {'easy' : (20, 77, 10), 'medium' : (40, 22, 5), 'hard' : (100, 9, 2)}

class Game:
    def __init__(self, screen, mode_play, difficult, start_x, start_y, end_x, end_y, time, step, gamename, username, maze = None, status = None):

        # general setup
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.img_ground = pygame.image.load('assets/tilemap/ground.png')
        self.img_bg = pygame.image.load('assets/tilemap/background.png')
        self.img_border = pygame.image.load('assets/tilemap/border.png')
        self.display_surface = pygame.surface.Surface((680, 680))

        self.mode_play = mode_play
        self.difficult = difficult
        self.gamename = gamename
        self.username = username
        self.step = step
        self.start = (start_x, start_y)
        self.end = (end_x, end_y)

        if maze is None:
            self.maze = Maze(self.display_surface, ATRIBUTES[difficult][0], start_x, start_y, end_x, end_y, ATRIBUTES[difficult][1], ATRIBUTES[difficult][2])
            self.maze.mazeGenerate()
        else:
            self.maze = maze

        if status is None:
            self.level = Level(self, int(self.maze.width - 2 * self.maze.wall_width))
        else:
            self.level = status

        self.menu = Display(self.screen, {'home' : (815, 589), 'new' : (938, 589), 'save' : (1061, 589), 'help' : (1184, 589)},
                            [(f'Name: {gamename}', (860, 300)), (f'Difficult: {difficult}', (860, 360)), (f'Mode: {mode_play}', (860, 420)), ('Time: 00:00', (860, 480))])
        self.menu.clock.get(time)

    def pack_data(self):
        data = {}
        data['mode_play'] = self.mode_play
        data['level'] = self.difficult
        data['start'] = self.start
        data['end'] = self.end
        data['time'] = self.menu.clock.pack()
        data['step'] = self.step
        data['gamename'] = self.gamename
        data['username'] = self.username
        data['maze'] = self.maze
        data['status'] = self.level
        return data

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
                self.pack_data()
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
                    if event.key == pygame.K_r:
                        pass

            pygame.display.update()
            self.clock.tick(FPS)
