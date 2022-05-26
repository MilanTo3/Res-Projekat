import socket
import threading

HEADER = 64
PORT = 5050
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
shotServer = "localhost"
shotPort = 5052

def receiveWriterMessage(conn):
    msg = ''
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
    return msg

def sendToReceiver(client, msg):
    
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)          
    client.send(msg.encode(FORMAT))

def setupClient():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((shotServer, shotPort))
    return client

def handle_client(conn):
    
    while True:
        msg = receiveWriterMessage(conn)
        relayLock.acquire()
        sendToReceiver(shotClient, msg)
        relayLock.release()

if __name__ == "__main__": # pragma: no cover
    
    shotClient = setupClient()    
    relayLock = threading.Lock()
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
