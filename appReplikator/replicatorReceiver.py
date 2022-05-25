import socket
import threading

HEADER = 64
PORT = 5052
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
shotServer = "localhost"
shotPort = 5053

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    sendThread.start()
    
    while True:
        receiveSenderMessage(conn)
    
    conn.close()
    
def receiveSenderMessage(conn):
    msg = ''
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg = conn.recv(msg_length).decode(FORMAT)
        
    listEl.append(msg)
    
    return msg

def periodicSend(listEl):
    pass
                    
if __name__ == "__main__": # pragma: no cover
    
    listEl = []
    sendThread = threading.Thread(target=periodicSend, args=(listEl, ))
    
    print("[STARTING] server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    conn, addr = server.accept()
    print(f"Replicator sender accepted.")
    handle_client(conn, addr)