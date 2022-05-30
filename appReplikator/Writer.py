#Writer component

from pydoc import cli
from random import randint
import socket
from statistics import fmean
import time

HEADER = 64
PORT = 5050
SERVER = 'localhost'
FORMAT = 'utf-8'
ADDRESS = (SERVER, PORT)

def createMessage():
    id = randint(1, 1000)
    water_consumed = randint(0, 240)
    return id, water_consumed

def formatMessage(id, cnsmp):
    formatedMessage = '{"id": ' + str(id) + ',"cnspn": ' + str(cnsmp) + '}'
    return formatedMessage

def setupClient():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDRESS)
    return client

def sendToSender(client, msg):
    messageLength = len(msg)
    sendlength = str(messageLength).encode(FORMAT)
    sendlength += b' ' * (HEADER - len(sendlength))
    client.send(sendlength)
    client.send(msg.encode(FORMAT))
    
#def periodicSend(msg):
 #   client = setupClient()
  #  
   # while True:
    #    sendToSender(client, msg)
     #   time.sleep(5000)
        
if __name__ == "__main__": # pragma : no cover
    
    client = setupClient()
        
    while True:    
        message = createMessage()
        fMessage = formatMessage(message[0], message[1])
        sendToSender(client, fMessage)
        print("Message sent")
        time.sleep(2)
    