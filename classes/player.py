import random

import pygame
from pygame import *

from config import *


class Player(pygame.sprite.Sprite):
    image = pygame.image.load(PATH_IMAGE + "bacterium.png")

    def __init__(self, *groups, sock, address, x, y):
        super().__init__(*groups)

        self.sock = sock
        self.address = address
        self.error = 0
        self.isLive = 1

        self.speed = 20
        self.force = PLAYER_SIZE

        Player.image = pygame.transform.scale(Player.image, (self.force, self.force))

        self.name = str(random.randint(100, 50000))

        self.skin = ""

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

        if self.skin != "":
            self.image = pygame.transform.scale(pygame.image.load(PATH_IMAGE + f"bacterium_{self.skin}.png"), (self.force, self.force))
        else:
            self.image = pygame.transform.scale(pygame.image.load(PATH_IMAGE + f"bacterium.png"), (self.force, self.force))


        self.rect = self.image.get_rect()

        self.rect.x = old_x
        self.rect.y = old_y

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
