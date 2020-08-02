import serial
import sqlite3
from datetime import datetime
import time

# establish serial connection
ArduinoData = serial.Serial('com3', 9600)  

# recieve RFID
def rfidkey_get():
    x = ArduinoData.readline()  # read ID
    String = x.rstrip()  # remove: \r\n
    card_id = String.decode()  # remove: b''
    return card_id

def sql(b_id):
    #establish sql database connection
    try:
        db_conn = sqliteConnection = sqlite3.connect('test.db')
        db_cursor = sqliteConnection.cursor()
        print('SQL CONNECTION PASSED!')
    except sqlite3.Error as error:
        print(f'SQL CONNECTION FAILED! ERROR : {error}')
    
    # see if rfid has acess
    name = db_cursor.execute("SELECT full_name FROM rfid_acess WHERE b_key IS ?;", (b_id,) )
    name = name.fetchone()
    if name != None:
        name = name[0]
    
    
    #commit_query
    db_conn.commit()
    
    #Recive current time stamp
    t = datetime.now()
    date_time = t.strftime('%Y-%m-%d %H:%M:%S')
    #Exexute query
    db_cursor.execute(
        "INSERT INTO rfid_history (date_time, b_key, full_name) VALUES(?, ?, ?);", (date_time, b_id, str(name)))
    #commit_query
    db_conn.commit()
    
    #sending data back to arduino 
    if name == None:
        ArduinoData.write(b'0')
        print('ACESS DENIED')
    else:
        ArduinoData.write(b'1')
        print('ACESS GRANTED')
      
    if sqliteConnection:
        sqliteConnection.close()
'''
while True:
    keyID = rfidkey_get()
    if keyID != None:
        sql(keyID)
        keyID = None
'''