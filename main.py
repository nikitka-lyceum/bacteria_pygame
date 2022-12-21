import socket

import pygame
from config import *

from classes.player import *
from classes.map import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client.connect((socket.gethostbyname(socket.gethostname()), 2500))

player_image = pygame.image.load(PATH_IMAGE + "bacterium.png")

def draw(screen):
    screen.fill((0, 0, 0))
    screen.blit(player_image,
                (WIDTH // 2 - player_image.get_width() // 2,
                HEIGHT // 2 - player_image.get_height() // 2)
                )
    pygame.display.update()


def main():
    global player_image
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

        send_data = [
            {"left": int(keys[K_a] or keys[K_LEFT]),
             "right": int(keys[K_d] or keys[K_RIGHT]),
             "up": int(keys[K_w] or keys[K_UP]),
             "down": int(keys[K_s] or keys[K_DOWN])}
        ]

        client.send(f"{send_data}".encode("utf-8"))
        size = client.recv(2**20).decode("utf-8")
        player_image = pygame.transform.scale(player_image, (int(size), int(size)))

        draw(screen)

if __name__ == '__main__':
    main()
