import json
import socket
import sys

import pygame
from pygame import *
from config import *

from classes import *

eat_image = pygame.image.load(PATH_IMAGE + "eat.png")
eat_image = pygame.transform.scale(eat_image, (EAT_SIZE, EAT_SIZE))

player_x, player_y, player_size = 0, 0, 100

isLive = -1

scale = 1
last_size = 0

camera = Camera()

pygame.init()
pygame.display.set_caption("Bacterium")
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
grid = Grid(screen)
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def die_screen(screen):
    intro_text = [f"Вы умерли"]

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        screen.fill(BACKGROUND_COLOR)

        # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
        # screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        pygame.display.update()

    main()


def start_screen(screen):
    global isLive

    isLive = 1
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.flip()
        clock.tick(FPS)


def draw(screen, visible):
    pygame.display.set_caption(f"{player_x}, {player_y}")
    screen.fill(BACKGROUND_COLOR)

    # Draw grid
    grid.draw()

    # Draw self
    screen.blit(pygame.transform.scale(pygame.image.load(PATH_IMAGE + "bacterium.png"),
                                       (player_size / scale, player_size / scale)),
                (WIDTH // 2 - player_size / scale // 2, HEIGHT // 2 - player_size / scale // 2))

    # Draw info
    font = pygame.font.Font(None, 20)
    size_text = font.render(f"Размер: {player_size}", True, (20, 255, 35))
    screen.blit(size_text, (WIDTH - size_text.get_width() - 5, 5))

    for i in visible:
        camera.update(player_x, player_y, player_size / scale, player_size / scale, WIDTH, HEIGHT)
        if i["type_obj"] == "Player":
            x = i["x"]
            y = i["y"]
            size = i["size"]
            x, y = camera.apply(player_x + x, player_y + y)

            screen.blit(pygame.transform.scale(pygame.image.load(PATH_IMAGE + "bacterium.png"), (size, size)), (x, y))

        else:
            x = i["x"]
            y = i["y"]
            x, y = camera.apply(player_x + x, player_y + y)
            color = tuple(map(int, i["color"].strip("()").split(', ')))

            eat_image_copy = eat_image.copy()
            eat_image_copy.fill(color)
            screen.blit(pygame.transform.scale(eat_image_copy, (EAT_SIZE / scale, EAT_SIZE / scale)), (x, y))

    # Update display
    pygame.display.update()


def main():
    global player_image, player_x, player_y, player_size, scale, last_size, isLive, WIDTH, HEIGHT

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    client.settimeout(2)
    client.connect((socket.gethostbyname(socket.gethostname()), 2600))

    client.send(f"{WIDTH};{HEIGHT}".encode("utf-8"))

    running = True
    while running:
        clock.tick(FPS)

        player_x = WIDTH // 2 - player_x
        player_y = HEIGHT // 2 - player_y

        WIDTH, HEIGHT = screen.get_width(), screen.get_height()

        # Update camera
        camera.update(player_x, player_y, player_size / scale, player_size / scale, WIDTH, HEIGHT)

        # Update grid position
        grid.update(player_x, player_y, scale, WIDTH, HEIGHT)

        # Check event
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[K_ESCAPE]:
                running = False
                terminate()

        try:
            # Send client data
            send_data = [
                {"left": int(keys[K_a] or keys[K_LEFT]),
                 "right": int(keys[K_d] or keys[K_RIGHT]),
                 "up": int(keys[K_w] or keys[K_UP]),
                 "down": int(keys[K_s] or keys[K_DOWN]),
                 "radius_review": f"{WIDTH};{HEIGHT}"}
            ]
            client.send(f"{send_data}".encode("utf-8"))

            # Apply server data
            server_data = json.loads(client.recv(4 ** 10).decode("utf-8").strip("[]").replace("'", '"'))
            visibles = server_data["visibles"]
            player_x = server_data["x"]
            player_y = server_data["y"]
            player_size = server_data["size"]
            isLive = server_data["isLive"]
            scale = server_data["scale"]

            if isLive == 0:
                running = False

            # Draw world
            draw(screen, visibles)

        except socket.timeout:
            pass

        except Exception as e:
            print(e)
            terminate()

    client.close()
    die_screen(screen)


if __name__ == '__main__':
    start_screen(screen)
    main()
    terminate()
