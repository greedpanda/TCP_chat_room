import socket
import threading

nickname = input("Enter a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 49999))    # Client connecting to the server.


# Receive function grabs the nickname if signaled with the flag.
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK_FLAG':
                client.send(nickname.encode('ascii'))
            else:
                print(message)

        except ConnectionError:
            print("An error occurred. Closing connection.")
            client.close()
            break


# Write function always waiting for a message
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive())
receive_thread.start()

write_thread = threading.Thread(target=write())
write_thread.start()
