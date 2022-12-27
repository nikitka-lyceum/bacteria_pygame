import copy
import json
import socket

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
for _ in range(10):
    map_objects.append(Eat())



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

            except Exception as e:
                print(e)

    visibles = [[] for _ in range(len(map_objects))]

    for i in range(len(map_objects)):
        for j in range(len(map_objects)):
            if str(map_objects[i]) == "Player" and id(map_objects[i]) != id(map_objects[j]):
                dict_x = map_objects[i].x - map_objects[j].x
                dict_y = map_objects[i].y - map_objects[j].y

                if abs(dict_x) <= 200 or abs(dict_y) <= 200:
                    type_obj = str(map_objects[j])
                    x = map_objects[j].x
                    y = map_objects[j].y
                    x = abs(dict_x)
                    y = abs(dict_y)


                    if type_obj == "Player":
                        size = map_objects[j].force
                        visibles[i].append(f"{type_obj} {x} {y} {size}")

                    else:
                        visibles[i].append(f"{type_obj} {x} {y}")



    for i in range(len(map_objects)):
        if str(map_objects[i]) == "Player":
            try:
                server_data = [
                    {'size': map_objects[i].force,
                     'name': map_objects[i].name,
                     'visibles': visibles[i]}
                ]
                # print(server_data)
                map_objects[i].sock.send(f"{server_data}".encode("utf-8"))
            except Exception:
                pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server_works = False

    # Draw screen
    screen.fill((10, 10, 10))

    for obj in map_objects:
        obj.draw(screen)

    pygame.display.update()

pygame.quit()
server.close()
