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
        self.timer = 0

    def update(self, player_x, player_y, scale, WIDTH, HEIGHT):
        # self.x = (0 - player_x) * -1
        # self.y = (0 - player_y) * -1

        if self.timer >= 200:
            self.x += 1
            self.y += 1

            self.timer = 0

        else:
            self.timer += 1

        self.size = scale * 20

        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT



    def draw(self):
        for i in range(self.x, WORLD_WIDTH):
            pygame.draw.line(self.screen, GRID_COLOUR,
                             [i * self.size, 0],
                             [i * self.size, WORLD_HEIGHT], 1)

        for i in range(self.x, WORLD_HEIGHT):
            pygame.draw.line(self.screen, GRID_COLOUR,
                             [0, i * self.size],
                             [WORLD_WIDTH, i * self.size], 1)