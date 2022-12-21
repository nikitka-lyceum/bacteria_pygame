import random

import pygame
from pygame import *

from config import *


class Player(pygame.sprite.Sprite):
    image = pygame.image.load(PATH_IMAGE + "bacterium.png")
    image = pygame.transform.scale(image, (100, 100))

    def __init__(self, *groups, sock, address, x, y):
        super().__init__(*groups)

        self.sock = sock
        self.address = address
        self.x = x
        self.y = y
        self.error = 0

        self.speed = 5
        self.size = 100
        self.force = 100

        self.name = "Pipka"

        self.image = Player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT // 2 - self.rect.height // 2

    def __str__(self):
        return "Player"

    def update(self, players_eats):
        for obj in players_eats:
            if self.rect.colliderect(obj.rect) and obj != self:
                if str(obj) == "Player":
                    if self.force > obj.force:
                        self.force += obj.force
                        obj.sock.close()
                        players_eats.remove(obj)

                elif str(obj) == "Eat":
                    self.force += obj.force
                    players_eats.remove(obj)



    def draw(self, screen):
        font = pygame.font.Font(None, 50)
        text = font.render(f"{self.name}: {self.force}", True, (20, 100, 250))

        screen.blit(text, (self.rect.x - self.image.get_width() // 2, self.rect.y - self.image.get_height()))
        screen.blit(Player.image, (self.rect.x, self.rect.y))