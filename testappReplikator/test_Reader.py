import socket, unittest, unittest.mock
import threading
from appReplikator.Reader import setupServer
import sys
sys.path.append('/.../appReplikator/DataBase.py')

HEADER = 64
PORT = 5053
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

class testReplicatorReceiver(unittest.TestCase):
    
    def test_setupServer(self):
            
        with unittest.mock.patch('appReplikator.Reader.socket.socket'):
            s=setupServer()
            s.bind.assert_called_with(('localhost', 5053))
