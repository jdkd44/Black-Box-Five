import sqlite3
import csv


#database options
dbName = 'BlackBox.db'
dbFolder = 'database/'

#export options
exportFile = 'BlackBox.csv'
exportPath = 'database/'


#clear database
def clearDatabase():
    remove_table = "DROP TABLE IF EXISTS sensor_data"           #SQLite statement to remove the existing table and it's data
    connection = sqlite3.connect(dbFolder + dbName)             #connect to database
    cur = connection.cursor()                                   #create cursor to move through database
    cur.execute(remove_table)                                   #remove table
    cur.execute("VACUUM")                                       #remove leftover data
    connection.commit()                                         #commit database changes
    connection.close()                                          #close database connection
    print("Database has been cleared")

#write data to database
def writeDB(currentTime, lateral_acc, vertical_acc, vel, height):
    logDB_all = "INSERT INTO sensor_data (entry_time, lateral_acceleration, vertical_acceleration, velocity, height) VALUES (?, ?, ?, ?, ?)"
    logDB_no_vel = "INSERT INTO sensor_data (entry_time, lateral_acceleration, vertical_acceleration, height) VALUES (?, ?, ?, ?)"
    connection = sqlite3.connect(dbFolder + dbName)             #connect to database
    cur = connection.cursor()                                   #create cursor to move through database
    try:
        with open(dbFolder + 'schema.sql') as f:                #open database format file
            connection.executescript(f.read())                  #create database tables if not existing

        if vel = "NULL":                                        #if there is velocity data (satellite has connection)
            cur.execute(logDB_all, (currentTime, lateral_acc, vertical_acc, vel, height))
        elif vel != "NULL":                                     #if there is not velocity data (satellite has no connection)
            cur.execute(logDB_no_vel, (currentTime, lateral_acc, vertical_acc, height))

        connection.commit()                                     #commit database changes
        connection.close()                                      #close database connection
        return True                                             #return true if successful
    except sqlite3.Error:
        connection.close()                                      #close database connection
        return False                                            #return false if theres an error
    


#read data from database
def readDB(entries = 1):
    connection = sqlite3.connect(dbFolder + dbName)             #connect to database
    cur = connection.cursor()                                   #create cursor to move through database
    exportScript = \
        "SELECT entry_time, lateral_acceleration, vertical_acceleration, velocity, height FROM \
         ( SELECT entry_time, lateral_acceleration, vertical_acceleration, velocity, height FROM sensor_data \
         ORDER BY entry_time DESC LIMIT " + str(entries) +") \
         ORDER BY entry_time ASC"
    cur.execute(exportScript)                                   #run the export script
    records = cur.fetchall()                                    #get export results

    time = [None for i in range(entries)]
    lateral_acc = [None for i in range(entries)]
    vertical_acc = [None for i in range(entries)]
    vel = [None for i in range(entries)]
    height = [None for i in range(entries)]

    for entry, row in enumerate(records):                       #seperate everything into individual sections
        time[entry], lateral_acc[entry], vertical_acc[entry], vel[entry], height[entry] = row

    return time, lateral_acc, vertical_acc, vel, height         #return results

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
    headers = [i[0] for i in cur.description]                   #get table headers


    with open(exportPath + exportFile, 'w', newline = '') as csvfile:
        export = csv.writer(csvfile, dialect = csv.excel)
        export.writerow(headers)
        for data in results:
            export.writerow(data)