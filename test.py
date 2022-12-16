import random

import pygame
from pygame import *


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0 for __ in range(width)] for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (j * self.cell_size + self.left, i * self.cell_size + self.top, self.cell_size, self.cell_size),
                    width=1)

                if self.board[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        (0, 240, 10),
                        (j * self.cell_size + self.left, i * self.cell_size + self.top, self.cell_size - 2,
                         self.cell_size - 2))

    def get_cell(self, mouse_pos):
        x, y = mouse_pos

        if x < self.left or x > self.width * self.cell_size + self.left:
            return None

        if y < self.top or y > self.height * self.cell_size + self.top:
            return None

        return ((x - self.left) // self.cell_size, (y - self.top) // self.cell_size)

    def on_click(self, cell_coords):
        if not (cell_coords is None):
            self.board[cell_coords[1]][cell_coords[0]] = abs(self.board[cell_coords[1]][cell_coords[0]] - 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


class Life(Board):
    def __init__(self, width, height):
        super().__init__(width, height)

    def next_move(self):
        new_board = self.board.copy()

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):

                left = (i - 1) % self.width
                right = (i + 1) % self.width
                above = (j - 1) % self.height
                below = (j + 1) % self.height

                this_cell = self.board[left][above] + self.board[i][above] + self.board[right][above] + \
                            self.board[left][j] + self.board[right][j] + \
                            self.board[i][below] + self.board[right][below]

                print(this_cell)

                if self.board[i][j] == 0 and this_cell == 3:
                    self.board[i][j] = 1

                elif self.board[i][j] == 1:
                    if this_cell == 2 or this_cell == 3:
                        self.board[i][j] = 1

                    else:
                        self.board[i][j] = 0

        self.board[:] = new_board[:]


n = int(input())
size = 50
isRun = False

pygame.init()
pygame.display.set_caption("Инициализация игры")
screen = pygame.display.set_mode((n * size + 40, n * size + 40))

# поле 5 на 7
board = Life(n, n)
board.set_view(20, 20, size)

fps = 60
clock = pygame.time.Clock()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEWHEEL:
            size += event.y
            board.set_view(20, 20, size)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                board.get_click(event.pos)

    if isRun:
        board.next_move()
        clock.tick(fps)

    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
