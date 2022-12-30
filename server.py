import copy
import json
import socket

import pygame.sprite

from classes import *
from config import *

server_works = True
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server.bind((socket.gethostbyname(socket.gethostname()), 2500))
server.setblocking(False)
server.listen()
print("Server Working...")

pygame.init()
pygame.display.set_caption("Server")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

map_objects = []
# for _ in range(150):
#     map_objects.append(Eat(color=(random.randint(0, 255),
#                      random.randint(0, 255),
#                      random.randint(0, 255))))

while server_works:
    clock.tick(FPS)

    map_objects = sorted(map_objects, key=lambda x: str(x) == "Player", reverse=True)

    # Connect new player
    try:
        client_socket, address = server.accept()
        client_socket.setblocking(True)
        new_player = Player(sock=client_socket,
                            address=address,
                            x=random.randint(0, WORLD_WIDTH),
                            y=random.randint(0, WORLD_HEIGHT))

        map_objects.append(new_player)

        print(f"Присоеденился {address}")
        for _ in range(100):
            map_objects.append(Eat(color=(random.randint(0, 255),
                                          random.randint(0, 255),
                                          random.randint(0, 255))))

    except Exception:
        pass

    for obj in map_objects:
        if str(obj) == "Player":
            try:
                keys = json.loads(obj.sock.recv(2 ** 10).decode("utf-8").strip("[]").replace("'", '"'))

                if keys["left"]:
                    obj.rect = obj.rect.move(-obj.speed, 0)

                if keys["right"]:
                    obj.rect = obj.rect.move(obj.speed, 0)

                if keys["up"]:
                    obj.rect = obj.rect.move(0, -obj.speed)

                if keys["down"]:
                    obj.rect = obj.rect.move(0, obj.speed)

            except Exception:
                pass

    visibles = [[] for _ in range(len(map_objects))]

    for i in range(len(map_objects)):
        for j in range(len(map_objects)):
            if str(map_objects[i]) == "Player":
                dict_x = map_objects[i].rect.x - map_objects[j].rect.x
                dict_y = map_objects[i].rect.y - map_objects[j].rect.y

                if abs(dict_x) <= map_objects[i].radius_review_x and abs(dict_y) <= map_objects[i].radius_review_y:
                    type_obj = str(map_objects[j])
                    x = map_objects[j].rect.x
                    y = map_objects[j].rect.y

                    if type_obj == "Player":
                        size = map_objects[j].force
                        visibles[i].append(f"{type_obj};{x};{y};{size}")

                    else:
                        color = map_objects[j].color
                        visibles[i].append(f"{type_obj};{x};{y};{color[0]},{color[1]},{color[2]}")

                if str(map_objects[j]) == "Player":
                    if abs(dict_x) <= map_objects[j].radius_review_x and abs(dict_y) <= map_objects[j].radius_review_y:
                        type_obj = str(map_objects[i])
                        x = map_objects[i].rect.x
                        y = map_objects[i].rect.y

                        if type_obj == "Player":
                            size = map_objects[i].force
                            visibles[j].append(f"{type_obj};{x};{y};{size}")

                        else:
                            color = map_objects[i].color
                            visibles[j].append(f"{type_obj};{x};{y};{color[0]},{color[1]},{color[2]}")

    for i in range(len(map_objects)):
        try:
            if str(map_objects[i]) == "Player":
                print(map_objects[i].force)
                server_data = [
                    {'x': map_objects[i].rect.x,
                     'y': map_objects[i].rect.y,
                     'size': map_objects[i].force,
                     'name': map_objects[i].name,
                     'visibles': visibles[i]}
                ]
                map_objects[i].sock.send(f"{server_data}".encode("utf-8"))

            map_objects[i].error = 0


        except Exception:
            try:
                map_objects.remove(map_objects[i])
            except Exception:
                pass

    for i in range(len(map_objects)):
        for j in range(i + 1, len(map_objects)):
            try:
                if str(map_objects[i]) == "Player":
                    if map_objects[i].rect.colliderect(map_objects[j].rect):
                        if str(map_objects[j]) == "Player":
                            if map_objects[i].force > map_objects[j].force:
                                map_objects[i].force += map_objects[j].force // 7
                                map_objects.remove(map_objects[j])

                            else:
                                map_objects[j].force += map_objects[i].force // 7
                                map_objects.remove(map_objects[i])

                        else:
                            map_objects[i].force = map_objects[j].force + map_objects[i].force
                            print(map_objects[i].force)
                            map_objects.remove(map_objects[j])
            except Exception:
                pass


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server_works = False

    # Draw screen
    screen.fill((10, 10, 10))

    for obj in map_objects:
        obj.draw(screen)
        obj.update()

    pygame.display.update()

pygame.quit()
server.close()
