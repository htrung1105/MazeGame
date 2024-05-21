import pygame
from tile import *
from player import Player
from maze_generator import Maze
from debug import debug
from settings import setting
pygame.init()

class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = setting.screen
        self.maze = setting.maze

        self.world_map = self.maze.convert()
        self.pause = False

        self.num_row = len(self.world_map)
        self.num_col = len(self.world_map[0])

        # sprite group setup
        self.visible_sprites = YSortCameraGroup(self.num_row, self.num_col)
        self.obstacles_sprites = pygame.sprite.Group()

        self.create_map()
        self.stack = []

    def create_map(self):
        for row_index, row in enumerate(self.world_map):
            for col_index, col in enumerate(row):
                x = col_index * setting.tilesize
                y = row_index * setting.tilesize
                if col == 'x':
                    Tile((x, y),[self.visible_sprites, self.obstacles_sprites])
                if col == 'p':
                    self.player = Player((x, y),[self.visible_sprites], self.obstacles_sprites)
                if col == 'e':
                    self.goal = Goal((x, y),[self.visible_sprites])

    def run(self):
        # winning
        if self.pause is False and self.goal.rect.colliderect(self.player.rect):
            self.player.rect = self.goal.rect
            self.player.pause = True
            self.pause = True
            self.visible_sprites.remove(self.goal)

        # save old pos of player
        pre_pos = self.player.rect.topleft

        # update and draw the game
        self.visible_sprites.custom_draw(self.player, self.num_row, self.num_col)
        self.visible_sprites.update()

        # get new pos of player
        now_pos = self.player.rect.topleft
        dx, dy = now_pos[0] - pre_pos[0], now_pos[1] - pre_pos[1]

        if dx != 0 or dy != 0:
            if dx > 0:
                status = 'right'
            elif dx < 0:
                status = 'left'
            elif dy > 0:
                status = 'down'
            else:
                status = 'up'

            if len(self.stack) > 0 and now_pos == self.stack[-1].pos:
                self.visible_sprites.remove(self.stack.pop())
            else:
                self.stack.append(Hint(pre_pos, status, [self.visible_sprites]))

        # return game is running or not
        return self.pause

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, num_row, num_col):

        # general setup
        super().__init__()
        self.display_surface = setting.screen
        self.width, self.height = self.display_surface.get_size()

        self.half_width = self.width // 2
        self.half_height = self.height // 2
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load("assets/tilemap/ground.png").convert_alpha()
        self.floor_surf = pygame.transform.smoothscale(self.floor_surf, (setting.tilesize * num_col, setting.tilesize * num_row))
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))

    def custom_draw(self, player, num_row, num_col):

        # getting the offset
        if player.rect.centerx <= self.half_width:
            self.offset.x = 0
        elif player.rect.centerx >= setting.tilesize * num_col - self.half_width:
            self.offset.x = max(self.width, setting.tilesize * num_col) - self.width
        else:
            self.offset.x = player.rect.centerx - self.half_width

        if player.rect.centery <= self.half_height:
            self.offset.y = 0
        elif player.rect.centery >= setting.tilesize * num_row - self.half_height:
            self.offset.y = max(self.height, setting.tilesize * num_row) - self.height
        else:
            self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)