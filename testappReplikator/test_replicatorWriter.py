from http import server
import threading
import socket, unittest, unittest.mock, re
from appReplikator.Writer import createMessage, formatMessage, setupClient, sendToSender
from appReplikator.replicatorReceiver import receiveSenderMessage

HEADER = 64
PORT = 5050
SERVER = 'localhost'
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
shotServer = "localhost"
shotPort = 5052

class test_replicatorWriter(unittest.TestCase):
    
    k = ''
    
    def runMockServer(self, recv):
        serverSocket = socket.socket()
        serverSocket.bind(('127.0.0.1', shotPort))
        serverSocket.listen()
        connection, address = serverSocket.accept()
        if recv:
            msg_length = connection.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                self.k = connection.recv(msg_length).decode(FORMAT)
        serverSocket.close()
        
    def runFakeClient(self):
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 5052))
        
        msg = 'Message'
        msg_length = len(msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(msg.encode(FORMAT))
        client.close()
        
    def test_clientSetup(self):
        
        server_thread = threading.Thread(target=self.runMockServer, args=(False, ))
        server_thread.start()
        
        client = setupClient()
        self.assertIsNotNone(client, "Client is not none. Socket successfully created.")
        client.close()
        
    def test_clientSetupException(self):
        
        server_thread = threading.Thread(target=self.runMockServer, args=(False, ))
        server_thread.start()
        
        raised = False
        
        try:
            setupClient()
        except:
            raised = True
        
        self.assertFalse(raised, "No exception raised")
        
    def test_address(self):
        
        with unittest.mock.patch('appReplikator.Writer.socket.socket'):
            c = setupClient()
            c.connect.assert_called_with(('localhost', 5050))
        
    def test_message(self):
        
        client_thread = threading.Thread(target=self.runFakeClient)
        sock = socket.socket()
        sock.bind(ADDRESS)
        sock.listen()
        client_thread.start()
        conn, addr = sock.accept()
        
        msg = receiveSenderMessage(conn)
        sock.close()
        self.assertEqual('Message', msg)
        
    def test_consumptionRange(self):
        
        testTuple = self.createMessage()
        self.assertTrue(0 <= testTuple[1] <= 240, "Water consumption is in range.")
        
    def test_messageFormat(self):
        
        message = self.formatMessage(2, 56)
        self.assertEqual(message, "{id: 2, cnspn: 56}", "Message was formated correctly.")
        
    def test_messageFormat1(self):
        message = self.formatMessage(7, 164)
        result = re.search("^{id: 7, cnspn: 164}$", message)
        self.assertTrue(result, "Message was formated correctly.")