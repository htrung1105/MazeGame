import pygame
from settings import *
from tile import Tile, Goal
from player import Player
from debug import debug

class Level:
    def __init__(self, screen, world_map):

        # get the display surface
        self.display_surface = screen
        self.world_map = world_map

        self.num_row = len(self.world_map)
        self.num_col = len(world_map[0])

        # sprite group setup
        self.visible_sprites = YSortCameraGroup(screen, self.num_row, self.num_col)
        self.obstacles_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(self.world_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites])
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites)
                if col == 'e':
                    self.goal = Goal((x, y), [self.visible_sprites])

    def run(self):
        # winning
        if self.goal.rect.colliderect(self.player.rect):
            print('Win!!')
            return True

        # update and draw the game
        self.visible_sprites.custom_draw(self.player, self.num_row, self.num_col)
        self.visible_sprites.update()
        return True

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, screen, num_row, num_col):

        # general setup
        super().__init__()
        self.display_surface = screen
        self.width, self.height = self.display_surface.get_size()
        self.half_width = self.width // 2
        self.half_height = self.height // 2
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load("assets/tilemap/ground.png").convert_alpha()
        self.floor_surf = pygame.transform.smoothscale(self.floor_surf, (TILESIZE * num_col, TILESIZE * num_row))
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))

    def custom_draw(self, player, num_row, num_col):

        # getting the offset
        if player.rect.centerx <= self.half_width:
            self.offset.x = 0
        elif player.rect.centerx >= TILESIZE * num_col - self.half_width:
            self.offset.x = max(self.width, TILESIZE * num_col) - self.width
        else:
            self.offset.x = player.rect.centerx - self.half_width

        if player.rect.centery <= self.half_height:
            self.offset.y = 0
        elif player.rect.centery >= TILESIZE * num_row - self.half_height:
            self.offset.y = max(self.height, TILESIZE * num_row) - self.height
        else:
            self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)