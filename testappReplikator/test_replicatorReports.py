from lib2to3.pgen2.token import EQUAL
from tempfile import tempdir
import unittest, unittest.mock
from ResProjekat.appReplikator.DataBase import readAllConsumers, updateConsumer
from appReplikator.DataBase import addConsumer, monthlyConsumerConsumption, monthlyStreetConsumption
    
class testReports(unittest.TestCase):
    
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