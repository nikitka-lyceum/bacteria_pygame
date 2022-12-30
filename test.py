import pygame

import config

pygame.init()
screen = pygame.display.set_mode((500, 500))

image1 = pygame.image.load(config.PATH_IMAGE + "eat.png")
image2 = pygame.image.load(config.PATH_IMAGE + "eat.png")

image1 = pygame.transform.scale(image1, (10, 10))
image2 = pygame.transform.scale(image2, (10, 10))

rect1 = image1.get_rect()
rect2 = image2.get_rect()

rect2.x = 9

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    print(rect1.colliderect(rect2))

    screen.fill((0, 0, 0))

    screen.blit(image1, (rect1.x, rect1.y))
    screen.blit(image2, (rect2.x, rect2.y))

    pygame.display.update()