import  socket
import threading

HOST = "127.0.0.1"
PORT = 7090
ENCODING = "utf-8"
HEADER = 1024
# ADDRESS = (HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []


# Broadcast
def broadcast(message):
    for client in clients:
        client.send(message)


# Handle
def handle(client):
    while True:
        try:
            message = client.recv(HEADER)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


# receive
def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")

        client.send("NICK".encode(ENCODING))
        nickname = client.recv(HEADER)

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to the server\n".encode(ENCODING))
        client.send("Connected to the server".encode(ENCODING))

        thread1 = threading.Thread(target=handle, args=(client, ))
        thread1.start()

print("[RUNNING] server running...")
receive()
