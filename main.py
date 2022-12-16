import pygame
from config import *
from classes.bacterium import *
from classes.player import *
from classes.eat import *

all_sprites = pygame.sprite.Group()

Bacterium(all_sprites)
Bacterium(all_sprites)
Bacterium(all_sprites)

Eat(all_sprites)
Eat(all_sprites)
Eat(all_sprites)
Eat(all_sprites)

def main():
    pygame.init()
    pygame.display.set_caption("Lost in the room")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    player = Player()


    def draw(screen):
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()

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

        for sprite in all_sprites:
            print(str(sprite))
            if str(sprite) == "Bacterium":
                sprite.check_enemy(all_sprites)

        player.check_enemy(all_sprites)
        player.update(event=keys, enemys=all_sprites)

        draw(screen)


if __name__ == '__main__':
    main()
