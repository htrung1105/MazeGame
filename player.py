import pygame
from settings import *
from utils import import_folder
from tile import Goal
from debug import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("assets/test/player.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)

        # graphics setup
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.5

        self.direction = pygame.math.Vector2()
        self.speed = 1

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = 'assets/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle' : [], 'left_idle' : [], 'up_idle' : [], 'down_idle' : []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status:
                self.status = self.status + '_idle'

    def move(self, speed):
        # Di chuyển mượt mà hơn
        frame = TILESIZE // speed    # mỗi bước di chuyển trong 1 frame
        time_delay = PING // frame   # thời gian delay sau mỗi frame

        for _ in range(frame):
            self.rect.x += self.direction.x * speed
            self.collision('horizontal')
            self.rect.y += self.direction.y * speed
            self.collision('vertical')
            pygame.time.delay(time_delay)
        if TILESIZE % speed != 0:
            self.rect.x += self.direction.x * (TILESIZE % speed)
            self.collision('horizontal')
            self.rect.y += self.direction.y * (TILESIZE % speed)
            self.collision('vertical')
            pygame.time.delay(time_delay)

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:    # moving right
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:    # moving left
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:  # moving down
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:  # moving up
                        self.rect.top = sprite.rect.bottom

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.rect.center)

    def update(self):
        self.input()
        self.get_status()
        self.move(self.speed)
        self.animate()

