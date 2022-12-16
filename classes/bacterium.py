import random

import pygame.sprite

from config import *

from pygame import *

pygame.init()


class Bacterium(pygame.sprite.Sprite):
    image = pygame.image.load(PATH_IMAGE + "bacterium.png")
    image = pygame.transform.scale(image, (100, 100))

    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = Bacterium.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.mask = pygame.mask.from_surface(self.image)

        self.force = 1
        self.speed = 5

    def __str__(self):
        return "Bacterium"

    def update(self):
        self.rect = self.rect.move(random.randrange(3) - 1,
                                   random.randrange(3) - 1)

    def check_enemy(self, enemys):
        for enemy in enemys:
            if pygame.sprite.collide_mask(self, enemy) and enemy != self:
                if str(enemy) == "Eat":
                    self.force += enemy.force
                    self.speed += enemy.speed

                    enemy.kill()

                elif self.force > enemy.force:
                    self.force += enemy.force
                    self.speed += enemy.speed

                    enemy.kill()
