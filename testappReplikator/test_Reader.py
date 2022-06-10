import socket, unittest, unittest.mock, sqlite3
import threading
import io
from appReplikator.Reader import consumerConsumption, readAllCons, setupServer, reciveReciverMessage, choose, addConsumerTroughConsole, readOneConsumer, jsonToObj
from appReplikator.DataBase import addConsumer, createTable
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
        
    @unittest.mock.patch('builtins.input')
    def test_addConsumerTroughConsole(self, input_patch):
        self.cleanTables()
        with self.assertRaises(Exception):
            input_patch.side_effect = ['1,Petar,Petroic,Danila_Kisa,5,31000,Uzice', '1,Petar,Petroic,Danila_Kisa,5,31000,Uzice']
            
            addConsumerTroughConsole('testDB.db')
            addConsumerTroughConsole('testDB.db')
    
    @unittest.mock.patch('builtins.input')
    def test_addConsumerTroughConsole_1(self, input_patch):
        self.cleanTables()
        
        input_patch.side_effect = ['id,Petar,Petroic,Danila_Kisa,street_num,city_num,Uzice']
        self.assertRaises(Exception, addConsumerTroughConsole, 'testDB.db')
        
    def test_readAllCons(self):
        self.cleanTables()
        addConsumer(1, 'Marko', 'Lazo' ,'Ulica' ,5 ,31000 ,'Uzice' ,'testDB.db')
        capturedOutput = io.StringIO()                  # Create StringIO object
        sys.stdout = capturedOutput                     #  and redirect stdout.
        readAllCons('testDB.db')                        # Call function.
        sys.stdout = sys.__stdout__                     # Reset redirect.
        
        self.assertEqual("<----------All Consumers---------->\n[(1, 'Marko', 'Lazo', 'Ulica', 5, 31000, 'Uzice')]\n", capturedOutput.getvalue())
          
    @unittest.mock.patch('builtins.input')
    def test_readOneConsumer(self, input_patch):
        self.cleanTables()
        addConsumer(1, 'Marko', 'Lazo' ,'Ulica' ,5 ,31000 ,'Uzice' ,'testDB.db')
        
        input_patch.side_effect = ['1']
        capturedOutput = io.StringIO()                  # Create StringIO object
        sys.stdout = capturedOutput                     #  and redirect stdout.
        readOneConsumer('testDB.db')                        # Call function.
        sys.stdout = sys.__stdout__                     # Reset redirect.
        
        self.assertEqual("Enter ID of Consumer: \n<----------Consumer---------->\n(1, 'Marko', 'Lazo', 'Ulica', 5, 31000, 'Uzice')\n", capturedOutput.getvalue())
        
    def test_jsonToObj(self):
        jsonn = '{"id":1,"cnspn":3};{"id":2,"cnspn":5}'
        jsonList = jsonToObj(jsonn)

        self.assertEqual(jsonList, [{"id":1, "cnspn":3}, {"id":2, "cnspn":5}])
        
        