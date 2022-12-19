import json
import random
import socket
import time
import pygame
from config import *
from classes.player import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server.bind(('localhost', 2500))
server.setblocking(False)
server.listen()
print("Working...")


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

players = []
server_works = True
while server_works:
    clock.tick(FPS)
    try:
        client_socket, address = server.accept()
        client_socket.setblocking(True)
        new_player = Player(all_sprites,
                            sock=client_socket,
                            address=address,
                            x=random.randint(0, WIDTH),
                            y=random.randint(0, HEIGHT))

        players.append(new_player)
        print(f"Присоеденился {address}")

    except Exception:
        pass

    for player in players:
        try:
            data = str(player.sock.recv(2**20).decode("utf-8"))

            data = data.replace("<", "").replace(">", "").replace("[", "").replace("]", "").replace("'", '"')
            print(data)
            keys = json.loads(data)
            print(keys)
            if keys["left"]:
                player.x -= player.speed
                print(5)

            if keys["right"]:
                player.x += player.speed

            if keys["up"]:
                player.y -= player.speed

            if keys["down"]:
                player.y += player.speed

        except Exception as e:
            print(e)

    for player in players:
        try:
            player.sock.send('Update'.encode("utf-8"))
        except Exception:
            pass



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server_works = False

    screen.fill((10, 10, 10))
    for player in players:
        player.draw(screen)
    pygame.display.update()

pygame.quit()
server.close()


# data = client_socket.recv(1024).decode("utf-8")
# print(data)
#
# HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
# content = 'Well done, buddy...'.encode("utf-8")
#
#
# client_socket.send(HDRS.encode('utf-8') + content)