import random

import pygame as pygame

from config import *

class Eat(pygame.sprite.Sprite):
    image = pygame.image.load(PATH_IMAGE + "eat.png")
    image = pygame.transform.scale(image, (20, 20))

    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = Eat.image
        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)

        self.force = random.randint(1, 5)


    def update(self):
        pass