import socket, unittest, unittest.mock, sqlite3
import threading
from appReplikator.Reader import setupServer, reciveReciverMessage, choose
from appReplikator.DataBase import createTable
import sys
sys.path.append('/.../appReplikator/DataBase.py')

HEADER = 64
PORT = 5053
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

class testReplicatorReceiver(unittest.TestCase):
    
    def run_fake_client(self):
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 5053))
        
        msg = 'Porukica'
        msg_length = len(msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(msg.encode(FORMAT))
        client.close()
    
    def cleanTables(self):
        conn = sqlite3.connect('testDB.db')
        cursor = conn.cursor()
        createTable("testDB.db")
        cursor.execute("""DELETE FROM consumers_info;""")
        cursor.execute("""DELETE FROM consumption_info;""")

        conn.commit()
        conn.close()
    
    def test_setupServer(self):
            
        with unittest.mock.patch('appReplikator.Reader.socket.socket'):
            s=setupServer()
            s.bind.assert_called_with(('localhost', 5053))

          
    def test_reciveReciverMessage(self):
        
        client_thread = threading.Thread(target=self.run_fake_client)
        sock = socket.socket()
        sock.bind(ADDR)
        sock.listen()
        client_thread.start()
        conn, addr = sock.accept()
        
        msg = reciveReciverMessage(conn)
        sock.close()
        self.assertEqual('Porukica', msg)

    @unittest.mock.patch('appReplikator.Reader.addConsumerTroughConsole')
    def test_Menu_1(self, func_patch):
        original_input = unittest.mock.builtins.input
        unittest.mock.builtins.input = lambda: "1"
        choose()
        unittest.mock.builtins.input = original_input
        func_patch.assert_called_once()
    
    @unittest.mock.patch('appReplikator.Reader.readAllCons')
    @unittest.mock.patch('appReplikator.Reader.readOneConsumer')
    @unittest.mock.patch('appReplikator.Reader.addConsumerTroughConsole')
    @unittest.mock.patch('builtins.input')
    def test_Menu_2(self, input_patch, func_patch_1, func_patch_2, func_patch_3):
        
        input_patch.side_effect = ['1', '2', '3']
        choose()
        choose()
        choose()
        func_patch_1.assert_called_once()
        func_patch_2.assert_called_once()
        func_patch_3.assert_called_once()