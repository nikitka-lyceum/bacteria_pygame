import random

import pygame.sprite

from config import *

class Eat(pygame.sprite.Sprite):
    image = pygame.image.load(PATH_IMAGE + "eat.png")
    image = pygame.transform.scale(image, (10, 10))

    def __init__(self, *groups, color):
        super().__init__(*groups)

        self.force = random.randint(1, 5)

        self.w_vision = WIDTH
        self.h_vision = HEIGHT

        self.image = Eat.image.copy()
        self.image.fill(color)

        self.color = color

        self.rect = self.image.get_rect()

        self.x = random.randint(1, WORLD_WIDTH)
        self.y = random.randint(1, WORLD_HEIGHT)

        self.error = 0

        self.rect.x = self.x
        self.rect.y = self.y

    def __str__(self):
        return "Eat"

    def update(self):
        self.x = self.rect.x
        self.y = self.rect.y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

