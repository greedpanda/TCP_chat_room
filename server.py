import socket
import threading

host = '127.0.0.1'  # localhost
port = 49999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except ConnectionError:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nickname.remove(nickname)
            broadcast(f"{nickname} left the chat room.".encode('ascii'))


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK_FLAG".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}.")
        broadcast(f"{nickname} joined the chat room.".encode('ascii'))
        client.send("Connected to the server".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server listening...")
receive()
