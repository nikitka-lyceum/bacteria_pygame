import json
import random
import socket
import time
import pygame
from config import *
from classes.eat import *
from classes.player import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server.bind((socket.gethostbyname(socket.gethostname()), 2500))
server.setblocking(False)
server.listen()
print("Working...")

pygame.init()
pygame.display.set_caption("Server")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

map_objects = []
for _ in range(10):
    map_objects.append(Eat())

server_works = True
while server_works:
    clock.tick(FPS)

    # Connect new player
    try:
        client_socket, address = server.accept()
        client_socket.setblocking(True)
        new_player = Player(sock=client_socket,
                            address=address,
                            x=random.randint(0, WIDTH),
                            y=random.randint(0, HEIGHT))

        map_objects.append(new_player)
        print(f"Присоеденился {address}")

    except Exception:
        pass

    # Check player command
    for obj in map_objects:
        try:
            data = str(obj.sock.recv(2 ** 20).decode("utf-8")).strip("[]").replace("'", '"')
            keys = json.loads(data)

            if keys["left"]:
                obj.rect.x -= obj.speed

            if keys["right"]:
                obj.rect.x += obj.speed

            if keys["up"]:
                obj.rect.y -= obj.speed

            if keys["down"]:
                obj.rect.y += obj.speed

        except Exception:
            pass

    # Send new state
    for obj in map_objects:
        try:
            obj.sock.send(f'"size": "{obj.force}"'.encode("utf-8"))
            obj.error = 0

        except Exception:
            if str(obj) == "Player":
                obj.error += 1

                if obj.error >= 500:
                    obj.sock.close()
                    map_objects.remove(obj)

    # Check event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server_works = False

    # Check visible
    visible = [[] for _ in range(len(map_objects))]

    for i in range(len(map_objects)):
        for j in range(i + 1, len(map_objects)):
            dict_x = map_objects[j].rect.x - map_objects[i].rect.x
            dict_y = map_objects[j].rect.y - map_objects[i].rect.y

            if abs(dict_x) <= map_objects[i].rect.x + WIDTH // 2 and abs(dict_y) <= map_objects[i].rect.x + HEIGHT // 2 and str(map_objects[i]) != "Eat":
                visible[i].append(f"{map_objects[i].rect.x},{map_objects[i].rect.y}")

    print(visible)

    # Send visible object
    for index, obj in enumerate(map_objects):
        try:
            obj.sock.send(" ".join(*visible).encode("utf-8"))

        except Exception:
            pass

    # Draw screen
    screen.fill((10, 10, 10))

    for obj in map_objects:
        obj.draw(screen)
        obj.update(map_objects)

    pygame.display.update()

pygame.quit()
server.close()
