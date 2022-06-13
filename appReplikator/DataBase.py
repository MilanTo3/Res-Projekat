from collections import defaultdict
import sqlite3
import random



def createTable(db_name = 'consumers.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS consumers_info(Id integer PRIMARY KEY, 
                                              Name text,
                                              Surname text, 
                                              Street text, 
                                              Street_num integer, 
                                              Post_num integer, 
                                              City text)""")
    

    cursor.execute("""CREATE TABLE IF NOT EXISTS consumption_info(Id integer, 
                                                Consumption real, 
                                                Month integer)""")
    conn.commit()
    conn.close()

def addConsumer(id, name, surname, street, street_num, post_num, city, db_name = 'consumers.db'):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    try:
        cur.execute("""INSERT INTO consumers_info(Id, Name, Surname, Street, Street_num, Post_num, City)
                                        VALUES(?, ?, ?, ?, ?, ?, ?)""", (id, name, surname, street, street_num, post_num, city))
    except sqlite3.IntegrityError:
        raise Exception("User with this ID already exists")
    
    conn.commit()
    conn.close()

def readConsumerInfo(id, db_name = 'consumers.db'):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute("""SELECT * FROM consumers_info WHERE Id = ?""", (id,))
    
    temp = cur.fetchone()
    conn.close()
    
    return temp

def readAllConsumers(db_name = 'consumers.db'):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute("""SELECT * FROM consumers_info""")
    
    temp = cur.fetchall()
    conn.close()

    return temp

def updateConsumer(id, cnspn, db_name = 'consumers.db', flag = 0):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    month = random.randint(1, 12)
    
    if flag != 0:
        month = 1

    cur.execute("""SELECT * FROM consumers_info WHERE Id = ?""", (id, ))
    consumer = cur.fetchone()
    if consumer == None:
        return 0

    cur.execute("""SELECT * FROM consumption_info WHERE Id = ? AND Month = ?""", (id, month))
    temp = cur.fetchone()

    if temp:
        cur.execute("""UPDATE consumption_info SET Consumption = Consumption + ? WHERE Id = ? AND Month = ?""", (cnspn, id, month))
    else:
        cur.execute("""INSERT INTO consumption_info VALUES(?,?,?)""", (id, cnspn, month))

    conn.commit()
    conn.close()

#def printConsumption():
#    conn = sqlite3.connect('consumers.db')
#    cur = conn.cursor()
#
#    cur.execute("""SELECT * FROM consumption_info""")
#    print(cur.fetchall())
#    conn.close()
    
if __name__ == "__main__": # pragma: no cover
    createTable()
    addConsumer(5,"aca", "nestor", "Partizanskih baza", 8, 21000, "Novi Sad")