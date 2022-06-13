from lib2to3.pgen2.token import EQUAL
from tempfile import tempdir
import unittest, unittest.mock, sqlite3
from appReplikator.DataBase import addConsumer, createTable, readConsumerInfo, readAllConsumers, updateConsumer

class testDataBase(unittest.TestCase):
    def setUp(self):
        conn = sqlite3.connect('testDB.db')
        cursor = conn.cursor()
        
        createTable('testDB.db')
        cursor.execute("""DELETE FROM consumers_info;""")
        cursor.execute("""DELETE FROM consumption_info;""")

        conn.commit()
        conn.close()

    def test_addConsumer(self):

        addConsumer(1, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade", "testDB.db")
        temp = readConsumerInfo(1, 'testDB.db')

        print(temp)
        self.assertEqual(temp[0], 1)

    def test_readConsumerInfo(self):
        addConsumer(1, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade", "testDB.db")
        temp = readConsumerInfo(1, 'testDB.db')

        print(temp)
        self.assertTupleEqual(temp, (1, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade"))
        self.assertIsInstance(temp, tuple)
    
    def test_readAllConsumers(self):
        addConsumer(1, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade", "testDB.db")
        addConsumer(2, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade", "testDB.db")
        addConsumer(3, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade", "testDB.db")
        addConsumer(4, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade", "testDB.db")

        temp = readAllConsumers('testDB.db')

        self.assertIsInstance(temp, list)
        self.assertListEqual(temp, [(1, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade"), (2, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade"), (3, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade"), (4, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade")])
    
    def test_updateConsumer_1(self):
        addConsumer(1, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade", "testDB.db")
        updateConsumer(1, 30, 'testDB.db', 1)

        conn = sqlite3.connect('testDB.db')
        c = conn.cursor()

        c.execute("""SELECT * FROM consumption_info WHERE Id = ? AND Month = ?""", (1, 1))
        temp = c.fetchone()

        self.assertEqual(temp, (1, 30, 1))        
        conn.close()

    def test_updateConsumer_2(self):
        addConsumer(1, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade", "testDB.db")
        updateConsumer(1, 30, 'testDB.db', 1)
        updateConsumer(1, 30, 'testDB.db', 1)

        conn = sqlite3.connect('testDB.db')
        c = conn.cursor()

        c.execute("""SELECT * FROM consumption_info WHERE Id = ? AND Month = ?""", (1, 1))
        temp = c.fetchone()

        self.assertEqual(temp, (1, 60, 1))        
        conn.close()
    
    def test_updateConsumer_3(self):
        x = updateConsumer(1, 155, 'testDB.db')
        self.assertEqual(x, 0)

    def test_CreateTable(self):
        createTable('testDB.db')

        conn = sqlite3.connect('testDB.db')
        c = conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        temp = c.fetchall()

        self.assertIsInstance(temp, list)
        self.assertEquals(temp, [("consumers_info",), ("consumption_info",)])
        