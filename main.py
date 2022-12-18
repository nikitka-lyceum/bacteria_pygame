import pygame
from config import *

from classes.player import *
from classes.map import *

map = Map(Player(), Player(), Player(), Player(), Player(), Player(), Player(), Player(), Player())
player = Player()


def draw(screen):
    screen.fill((0, 0, 0))
    player.draw(screen)
    pygame.display.update()


def main():
    pygame.init()
    pygame.display.set_caption("Bacterium")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        draw(screen)


if __name__ == '__main__':
    main()
