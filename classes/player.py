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

    def update(self, event=None):
        pass

    def draw(self, screen):
        screen.blit(Player.image, (self.rect.x, self.rect.y))