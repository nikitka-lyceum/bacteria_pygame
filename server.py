import copy
import json
import random
import socket
import threading
import time

from pygame import *
import pygame.sprite

from pickle import loads, dumps

from classes import *
from config import *

ip = socket.gethostbyname(socket.gethostname())
print(ip)

server_works = True
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server.bind((ip, 2600))
server.setblocking(False)
server.listen()
print("Server Working...")

pygame.init()
clock = pygame.time.Clock()

map_objects = []
timer = 0


def new_users():
    global map_objects

    while server_works:
        clock.tick(FPS)

        map_objects = sorted(map_objects, key=lambda x: str(x) == "Player", reverse=True)

        # Connect new player
        try:
            client_socket, address = server.accept()
            client_socket.setblocking(False)

            map_objects.append(Player(sock=client_socket,
                                      address=address,
                                      x=random.randint(0, WORLD_WIDTH),
                                      y=random.randint(0, WORLD_HEIGHT)))

            print(f"Присоеденился {address}")

        except Exception:
            pass


def update_timer():
    global timer, map_objects

    while server_works:
        clock.tick(FPS)

        list_count = [str(i) for i in map_objects]

        if timer >= 200 and list_count.count("Eat") <= 200:
            timer = 0
            for _ in range(random.randint(5, 20)):
                map_objects.append(Eat(color=(random.randint(0, 255),
                                              random.randint(0, 255),
                                              random.randint(0, 255))))

        else:
            timer += 1


def main():
    global server_works

    while server_works:
        clock.tick(FPS)

        # Find visible enemy
        visibles = [[] for _ in range(len(map_objects))]
        for i in range(len(map_objects)):
            for j in range(len(map_objects)):
                if str(map_objects[i]) == "Player" and map_objects[i] != map_objects[j]:
                    dict_x = map_objects[i].rect.x - map_objects[j].rect.x
                    dict_y = map_objects[i].rect.y - map_objects[j].rect.y

                    if abs(dict_x) <= map_objects[i].radius_review_x and abs(dict_y) <= map_objects[
                        i].radius_review_y:
                        type_obj = str(map_objects[j])

                        x = round(dict_x / map_objects[i].scale) * -1
                        y = round(dict_y / map_objects[i].scale) * -1

                        if type_obj == "Player":
                            size = round(map_objects[j].force // map_objects[i].scale)
                            j_data = {
                                'type_obj': type_obj,
                                'nickname': map_objects[j].name,
                                'x': x,
                                'y': y,
                                'size': size,
                                'skin': map_objects[j].skin,
                                'force': round(map_objects[j].force)
                            }
                            visibles[i].append(j_data)

                        else:
                            color = str(map_objects[j].color)
                            j_data = {
                                'type_obj': type_obj,
                                'x': x,
                                'y': y,
                                'color': color
                            }
                            visibles[i].append(j_data)

        # Check collide
        for i in range(len(map_objects)):
            for j in range(len(map_objects)):
                try:
                    if str(map_objects[i]) == "Player":
                        if map_objects[i].rect.colliderect(map_objects[j].rect):

                            if str(map_objects[j]) == "Player":
                                if map_objects[i].force > map_objects[j].force:
                                    map_objects[i].force += map_objects[j].force // 5
                                    map_objects[j].isLive = 0

                                elif map_objects[i].force < map_objects[j].force:
                                    map_objects[j].force += map_objects[i].force // 5
                                    map_objects[i].isLive = 0

                            else:
                                map_objects[i].force += map_objects[j].force
                                map_objects.remove(map_objects[j])


                except Exception:
                    pass

        for i in range(len(map_objects)):
            # Send server data
            try:
                map_objects[i].error = 0

                if str(map_objects[i]) == "Player":
                    server_data = [
                        {'x': map_objects[i].rect.x,
                         'y': map_objects[i].rect.y,
                         'size': round(map_objects[i].force),
                         'scale': map_objects[i].scale,
                         'isLive': map_objects[i].isLive,
                         'visibles': visibles[i]}
                    ]

                    map_objects[i].sock.send(f"{server_data}".encode("utf-8"))

                    if map_objects[i].isLive == 0:
                        raise Exception

                    # Handler command
                    try:
                        obj = map_objects[i]
                        keys = json.loads(obj.sock.recv(2 ** 10).decode("utf-8").strip("[]").replace("'", '"'))

                        obj.radius_review_x = int(keys["radius_review"].split(";")[0]) * obj.scale
                        obj.radius_review_y = int(keys["radius_review"].split(";")[1]) * obj.scale
                        obj.WIDTH = obj.radius_review_x
                        obj.HEIGHT = obj.radius_review_y

                        obj.name = keys["nickname"]
                        obj.skin = keys["skin"]

                        if keys["left"]:
                            if obj.rect.x - obj.speed >= 0:
                                obj.rect = obj.rect.move(-obj.speed, 0)

                            else:
                                obj.rect.x = 0

                        if keys["right"]:
                            if obj.rect.x + obj.speed + obj.force <= WORLD_WIDTH:
                                obj.rect = obj.rect.move(obj.speed, 0)

                            else:
                                obj.rect.x = WORLD_WIDTH - obj.force

                        if keys["up"]:
                            if obj.rect.y - obj.speed >= 0:
                                obj.rect = obj.rect.move(0, -obj.speed)

                            else:
                                obj.rect.y = 0

                        if keys["down"]:
                            if obj.rect.y + obj.speed + obj.force <= WORLD_HEIGHT:
                                obj.rect = obj.rect.move(0, obj.speed)

                            else:
                                obj.rect.y = WORLD_HEIGHT - obj.force

                        # Update obj
                        obj.update(obj.WIDTH, obj.HEIGHT)

                    except Exception:
                        pass

            except Exception:
                try:
                    map_objects[i].sock.close()
                    map_objects.remove(map_objects[i])
                except Exception:
                    pass

    pygame.quit()
    server.close()


if __name__ == '__main__':
    threading.Thread(target=new_users).start()
    threading.Thread(target=update_timer).start()
    threading.Thread(target=main).start()
