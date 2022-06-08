from collections import defaultdict
import sqlite3
import random
from Consumer import consumer


def createTable():
    conn = sqlite3.connect('consumers.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE consumers_info(Id integer PRIMARY KEY, 
                                              Name text,
                                              Surname text, 
                                              Street text, 
                                              Street_num integer, 
                                              Post_num integer, 
                                              City text)""")
    

    cursor.execute("""CREATE TABLE consumption_info(Id integer, 
                                                Consumption real, 
                                                Month integer)""")
    conn.commit()
    conn.close()