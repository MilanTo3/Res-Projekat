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

def addConsumer(id, name, surname, street, street_num, post_num, city):
    conn = sqlite3.connect('consumers.db')
    cur = conn.cursor()

    try:
        cur.execute("""INSERT INTO consumers_info(Id, Name, Surname, Street, Street_num, Post_num, City)
                                        VALUES(?, ?, ?, ?, ?, ?, ?)""", (id, name, surname, street, street_num, post_num, city))
    except sqlite3.IntegrityError:
        raise Exception("User with this ID already exists")
    
    conn.commit()
    conn.close()

def readConsumerInfo(id):
    conn = sqlite3.connect('consumers.db')
    cur = conn.cursor()

    cur.execute("""SELECT * FROM consumers_info WHERE Id = ?""", (id,))
    
    temp = cur.fetchone()
    conn.close()
    
    return temp

def readAllConsumers():
    conn = sqlite3.connect('consumers.db')
    cur = conn.cursor()

    cur.execute("""SELECT * FROM consumers_info""")
    
    temp = cur.fetchall()
    conn.close()

    return temp

def updateConsumer(id, cnspn):
    conn = sqlite3.connect('consumers.db')
    cur = conn.cursor()

    month = random.randint(1, 12)

    cur.execute("""SELECT * FROM consumption_info WHERE Id = ? AND Month = ?""", (id, month))
    temp = cur.fetchone()

    if temp:
        cur.execute("""UPDATE consumption_info SET Consumption = Consumption + ? WHERE Id = ? AND Month = ?""", (cnspn, id, month))
    else:
        cur.execute("""INSERT INTO consumption_info VALUES(?,?,?)""", (id, cnspn, month))

    conn.commit()
    conn.close()