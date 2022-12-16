import random

import pygame.sprite

from config import *

from pygame import *

pygame.init()

class Bacterium(pygame.sprite.Sprite):
    image = pygame.image.load(PATH_IMAGE + "bacterium.png")

    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = Bacterium.image
        self.rect = self.image.get_rect()

        self.speed = 2
        self.force = 2

    def update(self):
        self.rect = self.rect.move(random.randrange(3) - 1,
                                   random.randrange(3) - 1)


class Player(pygame.sprite.Sprite):
    image = pygame.image.load(PATH_IMAGE + "bacterium.png")

    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = Bacterium.image
        self.rect = self.image.get_rect()

        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT // 2 - self.rect.height // 2

        self.speed = 2
        self.force = 2

    def update(self, event=None, groups=None):
        for bacterium in groups:
            if event is not None:
                if event[K_a] or event[K_LEFT]:
                    bacterium.rect = bacterium.rect.move(self.speed, 0)

                if event[K_d] or event[K_RIGHT]:
                    bacterium.rect = bacterium.rect.move(-self.speed, 0)

                if event[K_w] or event[K_UP]:
                    bacterium.rect = bacterium.rect.move(0, self.speed)

                if event[K_s] or event[K_DOWN]:
                    bacterium.rect = bacterium.rect.move(0, -self.speed)

    def draw(self, screen):
        screen.blit(Player.image, (self.rect.x, self.rect.y))



