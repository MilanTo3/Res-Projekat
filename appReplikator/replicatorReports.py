from collections import defaultdict
import sqlite3
from unittest import case


def monthlyStreetConsumption(street, db_name = 'consumers.db'):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute("""SELECT Id FROM consumers_info WHERE Street = ?""", (street,))
    temp = cur.fetchall()

    if temp:
        cur.execute("""SELECT Consumption, Month FROM consumption_info WHERE Id IN (SELECT Id FROM consumers_info WHERE Street = ?)""", (street,))
        result = cur.fetchall() 
        sum = defaultdict(int)

        for i, k in result:
            sum[k] += i 

        print("Monthly water consumption for ", street, " is ", sum)
        conn.close()
        return sum
    else:
        conn.close()
        raise Exception("Desired street does not exist!")

def monthlyConsumerConsumption(id, db_name = 'consumers.db'):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute("""SELECT Id FROM consumption_info WHERE Id = ?""", (id,))
    temp = cur.fetchall()

    if temp:
        cur.execute("""SELECT Consumption, Month FROM consumption_info WHERE Id = ?""", (id,))
        result = cur.fetchall()
        sum = defaultdict(int)

        for i, k in result:
            sum[k] += i 

        print("Monthly water consumption for user with id:", id, " is ", sum)
        conn.close()
        return sum
    else:
        conn.close()
        raise Exception("Desired consumer does not exist!")
    
    
    if __name__ == "__main__": # pragma : no cover
        
        while True:
            
            print("[REPORTS] Choose number to recieve desired report:")
            print("1. Monthly water consumption by street")
            print("2. Monthly water consumption by consumer")
            
            if int(input()) == 1:
                print("Enter street name:")
                monthlyStreetConsumption(input())
            elif int(input()) == 2:
                print("Enter consumer id:")
                monthlyConsumerConsumption(input())
            else:
                print("Invalid input")
                
            