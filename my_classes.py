import random

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть x, y на смещение камеры
    def apply(self, x, y):
        return x + self.dx, y + self.dy

    # позиционировать камеру
    def update(self, x, y, w, h, WIDTH, HEIGHT):
        self.dx = -(x + w // 2 - WIDTH // 2)
        self.dy = -(y + h // 2 - HEIGHT // 2)

import pygame.sprite

from config import *


class Eat(pygame.sprite.Sprite):
    image = pygame.image.load(PATH_IMAGE + "eat.png")
    image = pygame.transform.scale(image, (EAT_SIZE, EAT_SIZE))

    def __init__(self, *groups, color):
        super().__init__(*groups)

        self.color = color

        self.force = random.randint(1, 5)
        self.error = 0

        self.image = Eat.image.copy()
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(1, WORLD_WIDTH)
        self.rect.y = random.randint(1, WORLD_HEIGHT)


        self.WIDTH = 0
        self.HEIGHT = 0

    def __str__(self):
        return "Eat"

    def update(self, *args):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


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


import random

import pygame
from pygame import *

from config import *


class Player(pygame.sprite.Sprite):

    def __init__(self, *groups, sock, address, x, y, a):
        super().__init__(*groups)
        image = pygame.image.load(PATH_IMAGE + f'{a}.png')
        self.sock = sock
        self.address = address
        self.error = 0
        self.isLive = 1

        self.speed = 20
        self.force = PLAYER_SIZE

        Player.image = pygame.transform.scale(Player.image, (self.force, self.force))

        self.name = str(random.randint(100, 50000))

        self.image = Player.image.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.scale = 1

        self.radius_review_x = -1
        self.radius_review_y = -1

    def __str__(self):
        return "Player"

    def update(self, WIDTH, HEIGHT):
        old_x = self.rect.x
        old_y = self.rect.y

        self.image = pygame.transform.scale(pygame.image.load(PATH_IMAGE + f"{self.a}.png"), (self.force, self.force))
        self.rect = self.image.get_rect()

        self.rect.x = old_x
        self.rect.y = old_y

        print(5)
        if self.radius_review_x != -1 and self.radius_review_y != -1:

            if (self.force >= self.radius_review_x / 6 or self.force >= self.radius_review_y / 6):
                self.scale *= 2
                self.speed -= 5
                self.radius_review_x = WIDTH * self.scale
                self.radius_review_y = HEIGHT * self.scale

            if self.force < self.radius_review_x / 12 and self.force < self.radius_review_y / 12:
                if self.scale > 1:
                    self.scale //= 2
                    self.speed += 5
                    self.radius_review_x = WIDTH * self.scale
                    self.radius_review_y = HEIGHT * self.scale

        self.force -= self.force / 11000

    def draw(self, screen):
        font = pygame.font.Font(None, 50)
        text = font.render(f"{self.name}: {self.force}", True, (20, 100, 250))

        screen.blit(text, (self.rect.x, self.rect.y - 5))
        screen.blit(self.image, (self.rect.x, self.rect.y))