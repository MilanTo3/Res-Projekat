from lib2to3.pgen2.token import EQUAL
from tempfile import tempdir
import unittest, unittest.mock, sqlite3
from appReplikator.DataBase import addConsumer, readAllConsumers, updateConsumer, createTable
from appReplikator.replicatorReports import  monthlyConsumerConsumption, monthlyStreetConsumption, menu
    
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

        _, temp = monthlyStreetConsumption("Banjica", "testDB.db")
        
        self.assertIsInstance(temp, dict)
        self.assertEquals(temp, {1: 30})

    def test_monthlyStreetConsumption_2(self):
        addConsumer(1, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade", "testDB.db")
        updateConsumer(1, 30, 'testDB.db', 1)
       
        self.assertEqual(monthlyStreetConsumption("d", 'testDB.db'), (0, 0))

    def test_monthlyConsumerConsumption_1(self):
        addConsumer(1, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade", "testDB.db")
        updateConsumer(1, 30, 'testDB.db', 1)
        
        _, temp = monthlyConsumerConsumption(1, "testDB.db")

        self.assertIsInstance(temp, dict)
        self.assertDictEqual(temp, {1: 30})

    def test_monthlyConsumerConsumption_2(self):
        addConsumer(1, "Nemanja", "Petrovic", "Banjica", 70, 11000, "Belgrade", "testDB.db")
        updateConsumer(1, 30, 'testDB.db', 1)

        self.assertEqual(monthlyConsumerConsumption(9, 'testDB.db'), (0, 0))
        
    @unittest.mock.patch('appReplikator.replicatorReports.monthlyStreetConsumption')
    @unittest.mock.patch('appReplikator.replicatorReports.monthlyConsumerConsumption')
    @unittest.mock.patch('builtins.input')
    def test_menu(self, input_patch, func_patch_1, func_patch_2):
        
        input_patch.side_effect = ['1', 'Partizanskih baza', '2', '5', '4', 'rec']
        menu()
        menu()
        x = menu()
        y = menu()
        func_patch_1.assert_called_once()
        func_patch_2.assert_called_once()
        self.assertEqual(x, 0)
        self.assertEqual(y, 1)
        
    