from lib2to3.pgen2.token import EQEQUAL
import socket
import threading
from appReplikator.DataBase import *
import json, sqlite3

HEADER = 64
PORT = 5053
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

class consumerConsumption:
    id = 0
    cnspn = 0

def setupServer():
    print("[STARTING] server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    
    return server

def handle_client(conn):
    while True:
        msg = reciveReciverMessage(conn)
        for obj in jsonToObj(msg):
            try:
                updateConsumer(obj['id'], obj['cnspn'])
            except: 
                raise Exception()
    
def jsonToObj(message):
    listEl = []
    params = message.split(';')
    for split in params:
        if len(split) > 0:
            jsonToObj: consumerConsumption = json.loads(split)
            listEl.append(jsonToObj)
    return listEl
    
def menuListing():
    
    while True:
        choose()
    
def choose():
        
        print("<----------Enter Option---------->")
        print("1. Add New Consumer.")
        print("2. List All Consumers.")
        print("3. List One Consumer by ID.")
        try:
            option = int(input())
        except:
            print("Input value must be an integer")
            return 1
    
        if option == 1:
            addConsumerTroughConsole(),
        elif option == 2: 
            readAllCons(),
        elif option == 3: 
            readOneConsumer()
        else:
            print("Nothing...")
            return 0
        
def readAllCons(db_name = 'consumers.db'):
    print("<----------All Consumers---------->")
    temp = readAllConsumers(db_name)
    print(str(temp))

def readOneConsumer(db_name = 'consumers.db'):
    print("Enter ID of Consumer: ")
    try:
        id = int(input())    
    except:
        print("Given value is not an integer")
        return 0
    
    print("<----------Consumer---------->")
    info = readConsumerInfo(id, db_name)
    print(str(info))

def reciveReciverMessage(conn):
    msg = ''
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
    return msg

def addConsumerTroughConsole(db_name = 'consumers.db'):
    print("<----------ADD Consumer---------->")
    print("Enter Data in Format ( break with , WITHOUT space): id,name,surname,street,street_num,post_num,city")
    data = str(input())
    data = data.split(',')
    
    try:
        addConsumer(int(data[0]), data[1], data[2], data[3], int(data[4]), int(data[5]), data[6], db_name)
    except sqlite3.IntegrityError:
        print("Consumer Already Exists!")
        return 0
    except Exception:
        print("Unregular Input of Consumer's Data!")
        return 1

if __name__ == "__main__": # pragma: no cover
      
    server = setupServer()
    print(f"[LISTENING] Server is listening on {SERVER}")
    conn, addr = server.accept()
    
    menuThread = threading.Thread(target=menuListing) 
    menuThread.start()
    
    handle_client(conn)