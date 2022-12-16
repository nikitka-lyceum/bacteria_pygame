import pygame
from config import *
from classes.bacterium import *


all_bacterium = pygame.sprite.Group()

Bacterium(all_bacterium)
Bacterium(all_bacterium)
Bacterium(all_bacterium)
Bacterium(all_bacterium)
Bacterium(all_bacterium)
Bacterium(all_bacterium)
Bacterium(all_bacterium)
Bacterium(all_bacterium)


def main():
    pygame.init()
    pygame.display.set_caption("Lost in the room")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    player = Player()

    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        screen.fill((0, 0, 0))
        all_bacterium.update()
        all_bacterium.draw(screen)

        player.update(event=keys, groups=all_bacterium)
        player.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
