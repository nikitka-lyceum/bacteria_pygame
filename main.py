import pygame
from config import *
from classes.bacterium import *
from classes.player import *
from classes.eat import *

def main():
    pygame.init()
    pygame.display.set_caption("Lost in the room")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    player = Player()

    def draw(screen):
        screen.fill((0, 0, 0))

        player.draw(screen)
        pygame.display.update()

    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        draw(screen)


if __name__ == '__main__':
    main()
