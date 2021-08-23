import socket
import threading

HOST = '127.0.0.1'
PORT = 5050
ADDRESS = (HOST, PORT)
HEADER = 1024
ENCODING = "utf-8"

server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server.bind(ADDRESS)

server.listen()

nicknames = []
clients = []


# Broadcast
def broadcast(message):
    for client in clients:
        client.send(message)


# Receive
def receive():
    while True:
        client, address = server.accept()
        print(f"Conntected with {str(address)}")

        client.send("!NICK".encode(ENCODING))
        nickname = client.recv(HEADER)

        nicknames.append(nickname)
        clients.append(client)

        print(f"nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to the server\n")
        client.send("Connected to the server".encode(ENCODING))

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()


# Handle
def handle(client):
    while True:
        try:
            message = client.recv(HEADER)
            print(f"{nicknames[clients.index(client)]} - \"{message}\"")

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


print("[RUNNING] server running...")
receive()
