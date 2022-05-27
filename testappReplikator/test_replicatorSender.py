import socket, unittest, unittest.mock
import threading
from appReplikator.replicatorSender import setupClient, receiveWriterMessage, sendToReceiver

HEADER = 64
PORT = 5050
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
shotServer = "localhost"
shotPort = 5052

class test_replicatorSender(unittest.TestCase):
    
    k = ''
    
    def run_mock_receiver(self, recv):
            
        server_sock = socket.socket()
        server_sock.bind(('127.0.0.1', 5052))
        server_sock.listen()
        conn, addr = server_sock.accept()
        if recv:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                self.k = conn.recv(msg_length).decode(FORMAT)
        server_sock.close()
        
    def test_setupClient1(self):
        
        server_thread = threading.Thread(target=self.run_mock_receiver, args=(False, ))
        server_thread.start()
        
        client = setupClient()
        self.assertIsNotNone(client, 'Client isnt none! Successfull connect call.')
        
    def test_setupClient2(self):
        
        server_thread = threading.Thread(target=self.run_mock_receiver, args=(False, ))
        server_thread.start()
        
        raised = False
        try:
            setupClient()
        except:
            raised = True
                    
        self.assertFalse(raised, 'Exception not raised.')
            
    def test_setupClient(self):
        
        server_thread = threading.Thread(target=self.run_mock_receiver)
        server_thread.start()

        with unittest.mock.patch('appReplikator.writer.socket.socket'):
            c = setupClient()
            c.connect.assert_called_with(ADDR)
        
    