import random

import pygame.sprite

from config import *

class Eat(pygame.sprite.Sprite):
    image = pygame.image.load(PATH_IMAGE + "eat.png")
    image = pygame.transform.scale(image, (10, 10))

    def __init__(self, *groups):
        super().__init__(*groups)

        self.force = random.randint(1, 5)

        self.image = Eat.image
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(1, WIDTH)
        self.rect.y = random.randint(1, HEIGHT)

    def __str__(self):
        return "Eat"

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

