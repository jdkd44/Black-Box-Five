import sqlite3

dbName = 'BlackBox.db'

#clear database
def clearDatabase():
    connection = sqlite3.connect(dbName)                        #connect to database
    cur = connection.cursor()                                   #create cursor to move through database
    with open('dbclear.sql') as f:                              #open database format file
        connection.executescript(f.read())                      #create database tables if not existing
    connection.commit()                                         #commit database changes
    connection.close()                                          #close database connection
    
#write data to database
def logData(time, lateral_acc, vertical_acc, vel, height):
    connection = sqlite3.connect(dbName)                        #connect to database
    cur = connection.cursor()                                   #create cursor to move through database
    with open('schema.sql') as f:                               #open database format file
        connection.executescript(f.read())                      #create database tables if not existing

    #data logging
    cur.execute("INSERT INTO sensor_data (entry_time, lateral_acceleration, vertical_acceleration, velocity, height) VALUES (?, ?, ?, ?, ?)", (currentTime, lateral_acc, vertical_acc, vel, height))

    connection.commit()                                         #commit database changes
    connection.close()                                          #close database connection

#read data from database
#def readData(entries):
