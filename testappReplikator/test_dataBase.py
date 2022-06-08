from lib2to3.pgen2.token import EQUAL
import unittest, unittest.mock, sqlite3
from ResProjekat.appReplikator.DataBase import readAllConsumers
from appReplikator.DataBase import addConsumer, createTable, readConsumerInfo

class testDataBase(unittest.TestCase):
    def setUp(self):
        conn = sqlite3.connect('testDB.db')
        cursor = conn.cursor()
        
        cursor.execute("""DELETE FROM consumers_info;""")

        conn.commit()
        conn.close()

    def test_addConsumer(self):

        addConsumer(1, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade", "testDB.db")
        temp = readConsumerInfo(1, 'testDB.db')

        print(temp)
        self.assertEqual(temp[0], 1)

    

    
