import socket, unittest, unittest.mock
import threading
from appReplikator.replicatorReceiver import setupClient, setupServer, receiveSenderMessage, makeDataString, sendToReader

HEADER = 64
PORT = 5052
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
shotServer = "localhost"
shotPort = 5053

class testReplicatorReceiver(unittest.TestCase):
    
    k = ''
    
    def run_mock_receiver(self, recv): # pragma: no cover
            
        server_sock = socket.socket()
        server_sock.bind(('127.0.0.1', shotPort))
        server_sock.listen()
        conn, addr = server_sock.accept()
        if recv:
            msg_length = conn.recv(HEADER).decode(FORMAT)
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
        
    def test_makeDataString(self):
        
        listEl1 = ['[id: 1, cnsmp: 3]', '[id: 1, cnsmp: 200]', '[id: 3, cnsmp: 23]']
        listEl2 = ['[id: 1, cnsmp: 20]']
        listEl3 = ['']
        
        data1 = makeDataString(listEl1)
        data2 = makeDataString(listEl2)
        data3 = makeDataString(listEl3)
        
        self.assertEqual(data1, '[id: 1, cnsmp: 3];[id: 1, cnsmp: 200];[id: 3, cnsmp: 23]')
        self.assertEqual(data2, '[id: 1, cnsmp: 20]')
        self.assertEqual(data3, '')
    
    def test_sendToReader(self):
        
        server_thread = threading.Thread(target=self.run_mock_receiver, args=(True, ))
        server_thread.start()
        
        c = setupClient()
        listEl = ['[id: 1, cnsmp: 2]', '[id: 4, cnsmp: 3]', '[id: 210, cnsmp: 34]']
        
        sendToReader(c, listEl)
        server_thread.join()
        self.assertEqual('[id: 1, cnsmp: 2];[id: 4, cnsmp: 3];[id: 210, cnsmp: 34]', self.k)
        