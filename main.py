import pygame
from config import *


def main():
    pygame.init()
    pygame.display.set_caption("Lost in the room")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        pygame.display.update()


if __name__ == '__main__':
    main()
