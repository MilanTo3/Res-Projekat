import socket, unittest, unittest.mock, sqlite3
import threading
from appReplikator.Reader import setupServer, reciveReciverMessage
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

    