import socket, unittest, unittest.mock
import threading
from appReplikator.replicatorSender import setupClient, setupServer, receiveWriterMessage, sendToReceiver, handle_client

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
        server_sock.bind(('127.0.0.1', shotPort))
        server_sock.listen()
        conn, addr = server_sock.accept()
        if recv:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                self.k = conn.recv(msg_length).decode(FORMAT)
        server_sock.close()
        
    def run_mock_receiver_multiple_connections(self):
        
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind(('127.0.0.1', shotPort))
        server_sock.listen()
        conn1, addr1 = server_sock.accept()
        conn2, addr2 = server_sock.accept()
        conn3, addr3 = server_sock.accept()
        
        conns = [conn1, conn2, conn3]
        
        k = ''
        for conn in conns:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                self.k += conn.recv(msg_length).decode(FORMAT)
        
    def run_fake_client(self):
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        
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
        
        x = setupClient()
        self.assertIsNone(x)
            
    def test_setupClient(self):

        with unittest.mock.patch('appReplikator.replicatorSender.socket.socket'):
            c = setupClient()
            c.connect.assert_called_with(('localhost', 5052))
            
    def test_setupServer(self):
        
        with unittest.mock.patch('appReplikator.replicatorSender.socket.socket'):
            s = setupServer()
            s.bind.assert_called_with(('localhost', 5050))
            
    def test_receiveWriterMessage(self):
        
        client_thread = threading.Thread(target=self.run_fake_client)
        sock = socket.socket()
        sock.bind(ADDR)
        sock.listen()
        client_thread.start()
        conn, addr = sock.accept()
        
        msg = receiveWriterMessage(conn)
        sock.close()
        self.assertEqual('Porukica', msg)
        
    def test_sendMessage_1(self):
        
        server_thread = threading.Thread(target=self.run_mock_receiver, args=(True, ))
        server_thread.start()
        
        lock = threading.Lock()
        c = setupClient()
        sendToReceiver(c, 'Porukica2', lock)
        
        server_thread.join() # Sacekamo da server primi poruku i setuje self.k na 'Porukica2'.
        self.assertEqual('Porukica2', self.k)
        
    def test_sendMessage_2(self):
        
        server_thread = threading.Thread(target=self.run_mock_receiver_multiple_connections)
        server_thread.start()
        
        relayLock = threading.Lock()
        client1_thread = threading.Thread(target=self.sendThreadWriterSim, args=(relayLock, ))
        client2_thread = threading.Thread(target=self.sendThreadWriterSim, args=(relayLock, ))
        client3_thread = threading.Thread(target=self.sendThreadWriterSim, args=(relayLock, ))

        client1_thread.start()
        client2_thread.start()
        client3_thread.start()
        
        server_thread.join()
        
        self.assertEqual('PorukaPorukaPoruka', self.k)
        
    def sendThreadWriterSim(self, lock):
        
        c1 = setupClient()
        sendToReceiver(c1, 'Poruka', lock)
        
    def test_handle_client(self):
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(ADDR)
        server_socket.listen()
        t = threading.Timer(2, self.run_fake_client)
        t.start()
        server_socket.accept()
        
        with unittest.mock.patch('appReplikator.replicatorSender.sendToReceiver'):
            k = handle_client(server_socket)
            self.assertEqual(k, 0)
