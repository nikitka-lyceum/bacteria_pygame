import json
import socket
from classes import *

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

                print(keys, "keys")

                if keys["left"]:
                    obj.rect = obj.rect.move(-obj.speed, 0)

                if keys["right"]:
                    obj.rect = obj.rect.move(obj.speed, 0)

                if keys["up"]:
                    obj.rect = obj.rect.move(0, -obj.speed)

                if keys["down"]:
                    obj.rect = obj.rect.move(0, obj.speed)

                continue

            except Exception as e:
                print(e)

    for obj in map_objects:
        if str(obj) == "Player":
            try:
                server_data = [
                    {'size': obj.force,
                     'name': obj.name,
                     'visible': []}
                ]
                print(server_data)
                obj.sock.send(f"{server_data}".encode("utf-8"))
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
