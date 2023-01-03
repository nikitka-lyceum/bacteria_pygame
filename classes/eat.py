import random

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
