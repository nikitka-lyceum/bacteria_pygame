import pygame
import random
from config import *

WIDTH, HEIGHT = (1000, 500)
FPS = 60
GRID_COLOUR = (150, 150, 150)
WORLD_WIDTH, WORLD_HEIGHT = (4000, 4000)
WIDTH_WINDOW, HEIGHT_WINDOW = 1000, 500
PLAYER_SIZE = 100
EAT_SIZE = 20

BACKGROUND_COLOR = (15, 15, 15)

PATH_DATA = "data/"
PATH_IMAGE = PATH_DATA + "image/"
PATH_ICON = PATH_DATA + "icon/"



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

        self.rect.x = random.randint(-WORLD_WIDTH * 3, WORLD_WIDTH * 3)
        self.rect.y = random.randint(-WORLD_HEIGHT * 3, WORLD_HEIGHT * 3)

    def __str__(self):
        return "Eat"

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Grid():
    def __init__(self, screen):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.start_size = 200
        self.size = self.start_size

    def update(self, r_x, r_y, L):
        self.size = self.start_size // L
        self.x = -self.size + (-r_x) % (self.size)
        self.y = -self.size + (-r_y) % (self.size)

    def draw(self):
        for i in range(WIDTH_WINDOW // self.size + 2):
            pygame.draw.line(self.screen, GRID_COLOUR,
                             [self.x + i * self.size, 0],
                             [self.x + i * self.size, HEIGHT_WINDOW], 1)

        for i in range(HEIGHT_WINDOW // 2 + 2):
            pygame.draw.line(self.screen, GRID_COLOUR,
                             [0, self.y + i * self.size],
                             [WIDTH_WINDOW, self.y + i * self.size], 1)

class Player(pygame.sprite.Sprite):
    image = pygame.image.load(PATH_IMAGE + "bacterium.png")

    def __init__(self, *groups, sock, address, x, y):
        super().__init__(*groups)

        self.sock = sock
        self.address = address
        self.error = 0
        self.isLive = 1

        self.speed = 20
        self.force = PLAYER_SIZE

        Player.image = pygame.transform.scale(Player.image, (self.force, self.force))

        self.name = str(random.randint(100, 50000))

        self.image = Player.image.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

        self.scale = 1

        self.radius_review_x = WIDTH
        self.radius_review_y = HEIGHT

    def __str__(self):
        return "Player"

    def update(self):
        old_x = self.rect.x
        old_y = self.rect.y

        self.image = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "bacterium.png"), (self.force, self.force))
        self.rect = self.image.get_rect()

        self.rect.x = old_x
        self.rect.y = old_y

        if (self.force >= self.radius_review_x / 4 or self.force >= self.radius_review_y / 4) and self.force <= 1100:
            self.scale *= 2
            self.speed -= 3
            self.radius_review_x = WIDTH * self.scale
            self.radius_review_y = HEIGHT * self.scale

        if self.force < self.radius_review_x / 8 and self.force < self.radius_review_y / 8:
            if self.scale > 1:
                self.scale //= 2
                self.speed += 3
                self.radius_review_x = WIDTH * self.scale
                self.radius_review_y = HEIGHT * self.scale

        self.force -= self.force / 16000

    def draw(self, screen):
        font = pygame.font.Font(None, 50)
        text = font.render(f"{self.name}: {self.force}", True, (20, 100, 250))

        screen.blit(text, (self.rect.x, self.rect.y - 5))
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть x, y на смещение камеры
    def apply(self, x, y):
        return x + self.dx, y + self.dy

    # позиционировать камеру
    def update(self, x, y, w, h):
        self.dx = -(x + w // 2 - WIDTH // 2)
        self.dy = -(y + h // 2 - HEIGHT // 2)