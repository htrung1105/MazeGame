import pygame
from pygame import Vector2

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size, direction=None):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.direction = direction

    def update(self, movement=(0, 0), speed=1):
        frame_movement = [movement[0] + self.velocity[0], movement[1] + self.velocity[1]]
        x, y = int(self.pos[0]), int(self.pos[1])
        is_wall = self.game.maze.grid[y][x]

        if (frame_movement[0] > 0 and is_wall.walls['right']) or (frame_movement[0] < 0 and is_wall.walls['left']):
            frame_movement[0] = 0

        if (frame_movement[1] > 0 and is_wall.walls['bottom']) or (frame_movement[1] < 0 and is_wall.walls['top']):
            frame_movement[1] = 0

        if (self.direction is not None) and ((frame_movement[0] > 0 and self.direction == 0) or (frame_movement[0] < 0 and self.direction == 1)):
            self.game.assets[self.type] = pygame.transform.flip(self.game.assets[self.type], True, False)
            self.direction = 1 - self.direction

        self.pos[0] += frame_movement[0] * speed
        self.pos[1] += frame_movement[1] * speed

        self.pos[0] = min(max(0, self.pos[0]), self.game.maze.size - 1)
        self.pos[1] = min(max(0, self.pos[1]), self.game.maze.size - 1)

    def render(self, surf):
        surf.blit(self.game.assets[self.type], self.game.assets[self.type].get_rect(center=self.game.maze.grid[int(self.pos[1])][int(self.pos[0])].center))
