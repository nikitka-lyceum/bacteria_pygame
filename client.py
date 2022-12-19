import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 2000))



print(client.recv(1024).decode("utf-8"))