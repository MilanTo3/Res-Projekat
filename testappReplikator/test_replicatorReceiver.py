import socket, unittest, unittest.mock
import threading
from appReplikator.replicatorReceiver import setupClient, setupServer, receiveSenderMessage

HEADER = 64
PORT = 5052
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
shotServer = "localhost"
shotPort = 5053

class testReplicatorReceiver(unittest.TestCase):
    
    def run_mock_receiver(self, recv):
            
        server_sock = socket.socket()
        server_sock.bind(('127.0.0.1', shotPort))
        server_sock.listen()
        conn, addr = server_sock.accept()
        if recv:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                self.k = conn.recv(msg_length).decode(FORMAT)
        server_sock.close()
        
    def run_fake_client(self):
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 5052))
        
        msg = 'Porukica'
        msg_length = len(msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(msg.encode(FORMAT))
        client.close()
        
    def test_setupClient1(self):
        
        server_thread = threading.Thread(target=self.run_mock_receiver, args=(False, ))
        server_thread.start()
        
        client = setupClient()
        self.assertIsNotNone(client, 'Client isnt none! Successfull connect call.')
        client.close()
        
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
        
        with unittest.mock.patch('appReplikator.replicatorReceiver.socket.socket'):
            c = setupClient()
            c.connect.assert_called_with(('localhost', 5053))
            
    def test_setupServer(self):
        
        with unittest.mock.patch('appReplikator.replicatorReceiver.socket.socket'):
            s=setupServer()
            s.bind.assert_called_with(('localhost', 5052))
            
    def test_receiveSenderMessage(self):
        
        client_thread = threading.Thread(target=self.run_fake_client)
        sock = socket.socket()
        sock.bind(ADDR)
        sock.listen()
        client_thread.start()
        conn, addr = sock.accept()
        
        msg = receiveSenderMessage(conn)
        sock.close()
        self.assertEqual('Porukica', msg)
            