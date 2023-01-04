import pygame

from config import *

class Grid():
    def __init__(self, screen):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.size = 1

        self.WIDTH = 0
        self.HEIGHT = 0

    def update(self, player_x, player_y, w, h, WIDTH, HEIGHT):
        self.dx = -(player_x + w // 2 - WIDTH // 2)
        self.dy = -(player_y + h // 2 - HEIGHT // 2)

        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT



    def draw(self):
        for i in range(self.WIDTH // self.size + 2):
            pygame.draw.line(self.screen, GRID_COLOUR,
                             [self.x + self.dx + i * self.size, 0],
                             [self.x + self.dx + i * self.size, self.HEIGHT], 1)

        for i in range(self.HEIGHT // 2 + 2):
            pygame.draw.line(self.screen, GRID_COLOUR,
                             [0, self.y + self.dy + i * self.size],
                             [self.WIDTH, self.y + self.dy + i * self.size], 1)