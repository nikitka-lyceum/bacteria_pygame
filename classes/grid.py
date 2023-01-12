import pygame

from config import *

class Grid():
    def __init__(self, screen):
        self.screen = screen
        self.x = 1
        self.y = 1
        self.size = 1

        self.WIDTH = 0
        self.HEIGHT = 0

        self.start_size = PLAYER_SIZE

    def update(self, r_x, r_y, L, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.size = (self.start_size // L) * 50
        self.x = -self.size + (-r_x) % (self.size)
        self.y = -self.size + (-r_y) % (self.size)

    def draw(self):
        for i in range(self.WIDTH // self.size + 2):
            pygame.draw.line(self.screen, GRID_COLOUR,
                             [self.x + i * self.size, 0],
                             [self.x + i * self.size, self.HEIGHT], 1)

        for i in range(self.HEIGHT // 2 + 2):
            pygame.draw.line(self.screen, GRID_COLOUR,
                             [0, self.y + i * self.size],
                             [self.WIDTH, self.y + i * self.size], 1)