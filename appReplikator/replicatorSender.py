import socket
import threading

HEADER = 64
PORT = 5050
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
shotServer = "localhost"
shotPort = 5052

def setupClient():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((shotServer, shotPort))
    return client

def handle_client(conn):
    #shotClient = setupClient()

if __name__ == "__main__": # pragma: no cover
    
    print("[STARTING] server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()

    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, ))
        thread.start()
        print(f'[Active Connections] {threading.activeCount() - 1}')
