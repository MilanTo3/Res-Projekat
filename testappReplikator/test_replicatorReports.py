from lib2to3.pgen2.token import EQUAL
from tempfile import tempdir
import unittest, unittest.mock, sqlite3
from appReplikator.DataBase import addConsumer, readAllConsumers, updateConsumer, createTable
from appReplikator.replicatorReports import  monthlyConsumerConsumption, monthlyStreetConsumption
    
class testReports(unittest.TestCase):
    
    def setUp(self):
        conn = sqlite3.connect('testDB.db')
        cursor = conn.cursor()
        
        createTable('testDb.db')
        cursor.execute("""DELETE FROM consumers_info;""")
        cursor.execute("""DELETE FROM consumption_info;""")

        conn.commit()
        conn.close()
    
    def test_monthlyStreetConsumption_1(self):
        addConsumer(1, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade", "testDB.db")
        updateConsumer(1, 30, 'testDB.db', 1)

        temp = monthlyStreetConsumption("Banjica", "testDB.db")

        self.assertIsInstance(temp, dict)
        self.assertEquals(temp, {1: 30})

    def test_monthlyStreetConsumption_2(self):
        addConsumer(1, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade", "testDB.db")
        updateConsumer(1, 30, 'testDB.db', 1)
       
        self.assertRaises(Exception, monthlyStreetConsumption, "Grbavica", "testDB.db")

    def test_monthlyConsumerConsumption_1(self):
        addConsumer(1, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade", "testDB.db")
        updateConsumer(1, 30, 'testDB.db', 1)
        
        temp = monthlyConsumerConsumption(1, "testDB.db")

        self.assertIsInstance(temp, dict)
        self.assertDictEqual(temp, {1: 30})

    def test_monthlyConsumerConsumption_2(self):
        addConsumer(1, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade", "testDB.db")
        updateConsumer(1, 30, 'testDB.db', 1)

        self.assertRaises(Exception, monthlyConsumerConsumption, 9, "testDB.db")