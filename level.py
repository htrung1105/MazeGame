import pygame
from tile import *
from player import Player
from maze_generator import Maze
from debug import debug

class Level:
    def __init__(self, screen, maze, tilesize):

        # get the display surface
        self.display_surface = screen
        self.maze = maze
        self.tilesize = tilesize

        self.world_map = maze.convert()
        self.pause = False
        self.hint = False

        self.num_row = len(self.world_map)
        self.num_col = len(self.world_map[0])

        # sprite group setup
        self.visible_sprites = YSortCameraGroup(screen, self.num_row, self.num_col, self.tilesize)
        self.obstacles_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(self.world_map):
            for col_index, col in enumerate(row):
                x = col_index * self.tilesize
                y = row_index * self.tilesize
                if col == 'x':
                    Tile((x, y), self.tilesize, [self.visible_sprites, self.obstacles_sprites])
                if col == 'p':
                    self.player = Player((x, y), self.tilesize, [self.visible_sprites], self.obstacles_sprites)
                if col == 'e':
                    self.goal = Goal((x, y), self.tilesize, [self.visible_sprites])

    def run(self):
        # winning
        if self.pause is False and self.goal.rect.colliderect(self.player.rect):
            self.player.rect = self.goal.rect
            self.player.pause = True
            self.pause = True
            self.visible_sprites.remove(self.goal)

        x, y = 0, 0
        nx, ny = 0, 0
        dir = None
        if self.hint is False:
            self.visible_sprites.remove(self.hint)
        else:
            x, y = self.player.get_position()
            nx, ny = self.maze.hint[x][y]
            if nx - x > 0:
                dir = 'right'
            elif nx - x < 0:
                dir = 'left'
            elif ny - y > 0:
                dir = 'down'
            else:
                dir = 'up'
            self.hint = Hint((ny * self.tilesize, nx * self.tilesize), self.tilesize, dir, [self.visible_sprites])

        # update and draw the game
        self.visible_sprites.custom_draw(self.player, self.num_row, self.num_col)
        self.visible_sprites.update()
        debug(self.display_surface, (self.hint, x, y, nx, ny, dir))
        return self.pause

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, screen, num_row, num_col, tilesize):

        # general setup
        super().__init__()
        self.display_surface = screen
        self.width, self.height = self.display_surface.get_size()
        self.tilesize = tilesize

        self.half_width = self.width // 2
        self.half_height = self.height // 2
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load("assets/tilemap/ground.png").convert_alpha()
        self.floor_surf = pygame.transform.smoothscale(self.floor_surf, (self.tilesize * num_col, self.tilesize * num_row))
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))

    def custom_draw(self, player, num_row, num_col):

        # getting the offset
        if player.rect.centerx <= self.half_width:
            self.offset.x = 0
        elif player.rect.centerx >= self.tilesize * num_col - self.half_width:
            self.offset.x = max(self.width, self.tilesize * num_col) - self.width
        else:
            self.offset.x = player.rect.centerx - self.half_width

        if player.rect.centery <= self.half_height:
            self.offset.y = 0
        elif player.rect.centery >= self.tilesize * num_row - self.half_height:
            self.offset.y = max(self.height, self.tilesize * num_row) - self.height
        else:
            self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)