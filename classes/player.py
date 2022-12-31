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

        self.speed = 15
        self.force = PLAYER_SIZE

        Player.image = pygame.transform.scale(Player.image, (self.force, self.force))

        self.name = str(random.randint(100, 50000))

        self.image = Player.image.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

        self.radius_review_x = WIDTH
        self.radius_review_y = HEIGHT

    def __str__(self):
        return "Player"

    def update(self):
        old_x = self.rect.x
        old_y = self.rect.y


        self.image = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "bacterium.png"), (self.force, self.force))
        self.rect = self.image.get_rect()

        self.rect.x = old_x
        self.rect.y = old_y

    def draw(self, screen):
        font = pygame.font.Font(None, 50)
        text = font.render(f"{self.name}: {self.force}", True, (20, 100, 250))

        screen.blit(text, (self.rect.x, self.rect.y - 5))
        screen.blit(self.image, (self.rect.x, self.rect.y))