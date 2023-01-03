import pygame

from config import *

class Grid():
    def __init__(self, screen):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.size = 1

    def update(self, player_x, player_y, scale):
        self.size = PLAYER_SIZE // scale
        self.x = -self.size + (player_x) % (self.size / scale)
        self.y = -self.size + (player_y) % (self.size / scale)



    def draw(self):
        for i in range(WIDTH // self.size + 2):
            pygame.draw.line(self.screen, GRID_COLOUR,
                             [self.x + i * self.size, 0],
                             [self.x + i * self.size, HEIGHT], 1)

        for i in range(HEIGHT // 2 + 2):
            pygame.draw.line(self.screen, GRID_COLOUR,
                             [0, self.y + i * self.size],
                             [WIDTH, self.y + i * self.size], 1)