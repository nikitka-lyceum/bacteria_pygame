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
player_name = ""
player_skin = random.choice(skins)
# player_skin = "poison"

isLive = -1

scale = 1
last_size = 0

camera = Camera()

pygame.init()
pygame.display.set_caption("Bacterium")
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()


def draw_nickname(nickname, force, x, y, size, scale):
    font = pygame.font.Font(None, 45 // scale)
    text = font.render(f"{nickname}. Размер: {force}", True, (0, 20, 210))
    screen.blit(text, (x, y - 45 // scale))


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
    global isLive, player_name

    isLive = 1
    intro_text = ["Bacterium", ""
                  "Правила игры очень просты,",
                  "Поедай своих противников и стань лучшим среди них",
                  "Удачи!",
                  "Чтобы начать игру нажмине Enter"]

    font = pygame.font.Font(None, 30)

    input_name = ""
    text_error = font.render("", True, (255, 0, 0))

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(input_name) <= 3:
                        text_error = font.render("Никнейм слишком короткий", True, (255, 0, 0))
                    elif len(input_name) > 15:
                        text_error = font.render("Никнейм слишком длинный", True, (255, 0, 0))
                    else:
                        player_name = input_name
                        return

                elif event.key == pygame.K_BACKSPACE:
                    input_name = input_name[:-1]

                else:
                    input_name += event.unicode

        screen.fill((0, 0, 0))

        screen.blit(text_error, (10, 300))
        screen.blit(font.render(f"Введите никнейм: {input_name}", True, (0, 210, 10)), (10, 250))

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



def draw(screen, visible):
    pygame.display.set_caption(f"{player_x}, {player_y}")
    screen.fill(BACKGROUND_COLOR)

    # Draw self
    screen.blit(pygame.transform.scale(pygame.image.load(PATH_IMAGE + f"bacterium_{player_skin}.png"),
                                       (player_size / scale, player_size / scale)),
                (WIDTH // 2 - player_size / scale // 2, HEIGHT // 2 - player_size / scale // 2))

    # Draw self NickName
    font = pygame.font.Font(None, 25)
    text = font.render(f"{player_name}. Размер: {player_size}", True, (0, 20, 210))
    screen.blit(text, (WIDTH // 2 - player_size // 2, HEIGHT // 2 - (player_size / scale)))

    # Draw info
    font = pygame.font.Font(None, 20)
    size_text = font.render(f"Размер: {player_size}", True, (20, 255, 35))
    pos_text = font.render(f"Позиция: {player_x}px, {player_y}px", True, (20, 255, 35))
    screen.blit(size_text, (WIDTH - size_text.get_width() - 5, 5))
    screen.blit(pos_text, (WIDTH - pos_text.get_width() - 5, 25))

    for i in visible:
        camera.update(player_x, player_y, player_size / scale, player_size / scale, WIDTH, HEIGHT)
        if i["type_obj"] == "Player":
            x = i["x"]
            y = i["y"]
            size = i["size"]
            skin = i["skin"]
            force = i["force"]
            nickname = i["nickname"]

            x, y = camera.apply(player_x + x, player_y + y)
            draw_nickname(nickname, force, x, y, size, scale)

            if skin != "":
                screen.blit(pygame.transform.scale(pygame.image.load(PATH_IMAGE + f"bacterium_{skin}.png"), (size, size)), (x, y))
            else:
                screen.blit(pygame.transform.scale(pygame.image.load(PATH_IMAGE + f"bacterium.png"), (size, size)), (x, y))



        else:
            x = i["x"]
            y = i["y"]
            x, y = camera.apply(player_x + x, player_y + y)
            color = tuple(map(int, i["color"].strip("()").split(', ')))

            eat_image.fill(color)
            screen.blit(pygame.transform.scale(eat_image, (EAT_SIZE / scale, EAT_SIZE / scale)), (x, y))

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
                 "radius_review": f"{WIDTH};{HEIGHT}",
                 "nickname": player_name,
                 "skin": player_skin}
            ]
            client.send(f"{send_data}".encode("utf-8"))

            # Apply server data
            server_data = json.loads(client.recv(4 ** 10).decode("utf-8").strip("[]").replace("'", '"'))
            print(server_data)
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
            pass

    client.close()
    die_screen(screen)


if __name__ == '__main__':
    start_screen(screen)
    main()
    terminate()
