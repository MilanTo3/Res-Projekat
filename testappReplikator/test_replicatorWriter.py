import threading
import socket, unittest, unittest.mock, re
from appReplikator.Writer import createMessage, formatMessage, sendToSender, setupClient

HEADER = 64
PORT = 5050
SERVER = 'localhost'
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
shotServer = "localhost"
shotPort = 5050

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
        
    def test_messageFormat(self):
        
        message = formatMessage(2, 56)
        self.assertEqual(message, '{"id": 2,"cnspn": 56}', "Message was formated correctly.")
        
    def test_messageFormat1(self):
        message = formatMessage(7, 164)
        result = re.search('{"id": \d+,"cnspn": \d+}', message)
        self.assertTrue(result, "Message was formated correctly.")
        
    def test_consumptionRange(self):
            
        testTuple = createMessage()
        self.assertTrue(0 <= testTuple[1] <= 240, "Water consumption is in range.")
        
    def test_sendMessage(self):
        
        server_thread = threading.Thread(target=self.runMockServer, args=(True, ))
        server_thread.start()
        
        c = setupClient()
        
        sendToSender(c, 'Porukica')
        server_thread.join()
        self.assertEqual('Porukica', self.k)
        