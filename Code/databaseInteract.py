import sqlite3
import csv


#database options
dbName = 'BlackBox.db'
dbFolder = 'database/'

#export options
exportFile = 'BlackBox.csv'
exportPath = ''


#clear database
def clearDatabase():

    remove_table = "DROP TABLE IF EXISTS sensor_data"           #SQLite statement to remove the existing table and it's data

    connection = sqlite3.connect(dbFolder + dbName)             #connect to database
    cur = connection.cursor()                                   #create cursor to move through database
    cur.execute(remove_table)                                   #remove table
    connection.commit()                                         #commit database changes
    connection.close()                                          #close database connection

#write data to database
def writeDB(currentTime, lateral_acc, vertical_acc, vel, height):
    connection = sqlite3.connect(dbFolder + dbName)             #connect to database
    cur = connection.cursor()                                   #create cursor to move through database
    with open(dbFolder + 'schema.sql') as f:                    #open database format file
        connection.executescript(f.read())                      #create database tables if not existing

    #log data
    cur.execute("INSERT INTO sensor_data (entry_time, lateral_acceleration, vertical_acceleration, velocity, height) VALUES (?, ?, ?, ?, ?)", (currentTime, lateral_acc, vertical_acc, vel, height))

    connection.commit()                                         #commit database changes
    connection.close()                                          #close database connection

#read data from database
def readDB(entries = 20):
    connection = sqlite3.connect(dbFolder + dbName)             #connect to database
    cur = connection.cursor()                                   #create cursor to move through database
    readScript = \
        "SELECT entry_time, lateral_acceleration, vertical_acceleration, velocity, height FROM \
         ( SELECT entry_time, lateral_acceleration, vertical_acceleration, velocity, height FROM sensor_data \
         ORDER BY entry_time DESC LIMIT " + str(entries) +") \
         ORDER BY entry_time ASC"
    cur.execute(readScript)
    connection.close()                                      #run the export script
    return cur.fetchall()                                       #get and return export results

#export database to csv file
def exportDB():

    connection = sqlite3.connect(dbFolder + dbName)             #connect to database
    cur = connection.cursor()                                   #create cursor to move through database
    exportScript = \
        "SELECT entry_time, lateral_acceleration, vertical_acceleration, velocity, height \
         FROM sensor_data \
         ORDER BY entry_time"
    cur.execute(exportScript)                                   #run the export script
    results = cur.fetchall()                                    #get export results
    connection.close() 
    headers = [i[0] for i in cur.description]                   #get table headers


    with open(exportPath + exportFile, 'w', newline = '') as csvfile:
        export = csv.writer(csvfile, dialect = csv.excel)
        export.writerow(headers)
        for data in results:
            export.writerow(data)