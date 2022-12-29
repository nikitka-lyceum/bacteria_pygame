import json
import socket

import pygame
from config import *

from classes import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client.connect((socket.gethostbyname(socket.gethostname()), 2500))

player_image = pygame.image.load(PATH_IMAGE + "bacterium.png")
player_image = pygame.transform.scale(player_image, (100, 100))
eat_image = pygame.image.load(PATH_IMAGE + "eat.png")
eat_image = pygame.transform.scale(eat_image, (10, 10))

player_x, player_y = 0, 0

def draw(screen, visible):
    screen.fill((0, 0, 0))
    screen.blit(player_image, (player_x, player_y))

    for i in visible:
        if "Player" in i:
            x, y, size = list(map(int, i.replace("Player", "").split(";")[1:]))
            screen.blit(player_image, (x, y))
        else:
            type_obj, x, y, color = i.split(";")
            print(i)
            x = int(x)
            y = int(y)
            color = tuple(map(int, color.split(",")))
            eat_image_copy = eat_image.copy()
            eat_image_copy.fill(color)
            screen.blit(eat_image_copy, (x, y))

    pygame.display.update()


def main():
    global player_image, player_x, player_y
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
        server_data = json.loads(client.recv(2 ** 10).decode("utf-8").strip("[]").replace("'", '"'))
        visibles = server_data["visibles"]
        player_x = server_data["x"]
        player_y = server_data["y"]


        draw(screen, visibles)

if __name__ == '__main__':
    main()
