import pygame
from pygame import *

from config import *

class Player(pygame.sprite.Sprite):
    image = pygame.image.load(PATH_IMAGE + "bacterium.png")
    image = pygame.transform.scale(image, (100, 100))

    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = Player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT // 2 - self.rect.height // 2

        self.force = 1
        self.speed = 5

    def update(self, event=None, enemys=None):
        for enemy in enemys:
            if event[K_a] or event[K_LEFT]:
                enemy.rect = enemy.rect.move(self.speed, 0)

            if event[K_d] or event[K_RIGHT]:
                enemy.rect = enemy.rect.move(-self.speed, 0)

            if event[K_w] or event[K_UP]:
                enemy.rect = enemy.rect.move(0, self.speed)

            if event[K_s] or event[K_DOWN]:
                enemy.rect = enemy.rect.move(0, -self.speed)

    def draw(self, screen):
        screen.blit(Player.image, (self.rect.x, self.rect.y))