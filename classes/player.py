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
        self.x = x
        self.y = y
        self.error = 0

        self.speed = 15
        self.force = 100

        Player.image = pygame.transform.scale(Player.image, (self.force, self.force))

        self.name = str(random.randint(100, 50000))

        self.image = Player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT // 2 - self.rect.height // 2

        self.radius_review_x = WIDTH
        self.radius_review_y = HEIGHT

    def __str__(self):
        return "Player"

    def update(self):
        self.x = self.rect.x
        self.y = self.rect.y

    def draw(self, screen):
        font = pygame.font.Font(None, 50)
        text = font.render(f"{self.name}: {self.force}", True, (20, 100, 250))

        screen.blit(text, (self.rect.x - self.image.get_width() // 2, self.rect.y - self.image.get_height()))
        screen.blit(Player.image, (self.rect.x, self.rect.y))