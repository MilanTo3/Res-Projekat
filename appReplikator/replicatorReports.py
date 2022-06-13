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

        conn.close()
        return street, sum
    else:
        conn.close()
        print("Desired street does not exist!")
        return 0, 0

def monthlyConsumerConsumption(id, db_name = 'consumers.db'):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    
    cur.execute("""SELECT Id FROM consumers_info WHERE Id = ?""", (id,))
    temp = cur.fetchall()

    if temp:
        cur.execute("""SELECT Consumption, Month FROM consumption_info WHERE Id = ?""", (id,))
        result = cur.fetchall()
        sum = defaultdict(int)

        for i, k in result:
            sum[k] += i 

        conn.close()
        return id, sum
    else:
        conn.close()
        print("Desired consumer does not exist!")
        return 0, 0
    
def menu():
        
    print("[REPORTS] Choose number to recieve desired report:")
    print("1. Monthly water consumption by street")
    print("2. Monthly water consumption by consumer")
    
    try:
       x = int(input())
    except:
        print("Given value is not an integer")
        return 1
    
    if x == 1:
        print("Enter street name:")
        inValue = input()
        
        result = monthlyStreetConsumption(inValue)
        if result != (0, 0):
            print("Monthly water consumption for street", result[0])
            for key, value in sorted(result[1].items()):
                print(f"Month:{key}  Consumption:{value}")
    elif x == 2:
        print("Enter consumer id:")
        try:
            inValue = int(input())
        except:
            print("Given value is not an integer.")
            return 2
        result = monthlyConsumerConsumption(inValue)
        if result != (0, 0):
            print("Monthly water consumption for consumer with id:", result[0])
            for key, value in sorted(result[1].items()):
                print(f"Month:{key}  Consumption:{value}")
    else:
        print("Invalid input")
        return 0
    
    
if __name__ == "__main__": # pragma: no cover
    
    while True:
        menu()
                
            