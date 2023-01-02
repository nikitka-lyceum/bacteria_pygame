import json
import socket

import pygame
from config import *

from classes import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client.connect((socket.gethostbyname(socket.gethostname()), 2600))

eat_image = pygame.image.load(PATH_IMAGE + "eat.png")
eat_image = pygame.transform.scale(eat_image, (EAT_SIZE, EAT_SIZE))

player_x, player_y, player_size = 0, 0, 100

scale = 1
last_size = 0

camera = Camera()


def draw(screen, visible):
    screen.fill((10, 10, 10))

    screen.blit(pygame.transform.scale(pygame.image.load(PATH_IMAGE + "bacterium.png"),
                                       (player_size / scale, player_size / scale)),
                (WIDTH // 2 - player_size / scale // 2, HEIGHT // 2 - player_size / scale // 2))

    pygame.display.set_caption(f"{player_x}, {player_y}")

    font = pygame.font.Font(None, 20)
    size_text = font.render(f"Размер: {player_size}", True, (20, 255, 35))
    screen.blit(size_text, (WIDTH - size_text.get_width() - 5, 5))

    for i in visible:
        camera.update(player_x, player_y, player_size / scale, player_size / scale)
        if "Player" in i:
            x, y, size = list(map(int, i.replace("Player", "").split(";")[1:]))
            x, y = player_x + x, player_y + y
            x, y = camera.apply(x, y)

            screen.blit(pygame.transform.scale(pygame.image.load(PATH_IMAGE + "bacterium.png"), (size, size)), (x, y))
        else:
            type_obj, x, y, color = i.split(";")
            x, y = player_x + int(x), player_y + int(y)
            x, y = camera.apply(int(x), int(y))
            color = tuple(map(int, color.split(",")))
            eat_image_copy = eat_image.copy()
            eat_image_copy.fill(color)
            screen.blit(pygame.transform.scale(eat_image_copy, (EAT_SIZE / scale, EAT_SIZE / scale)), (x, y))

    pygame.display.update()


def main():
    global player_image, player_x, player_y, player_size, scale, last_size
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
        server_data = json.loads(client.recv(4 ** 10).decode("utf-8").strip("[]").replace("'", '"'))
        visibles = server_data["visibles"]
        player_x = server_data["x"]
        player_y = server_data["y"]
        player_size = round(server_data["size"])
        scale = server_data["scale"]

        draw(screen, visibles)


if __name__ == '__main__':
    main()
