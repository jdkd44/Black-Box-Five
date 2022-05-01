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
    with open(dbFolder + 'schema.sql') as f:                    #open database format file
        connection.executescript(f.read())                      #create database tables if not existing
    connection.commit()                                         #commit database changes
    connection.close()                                          #close database connection
    print("Database has been cleared")

#write data to database
def writeDB(currentTime, x_acc, y_acc, z_acc, vel, height, fix, lon = None, lat = None):
    logDB_all = "INSERT INTO sensor_data (entry_time, x_acceleration, y_acceleration, z_acceleration, velocity, height, longitude, latitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    logDB_no_vel = "INSERT INTO sensor_data (entry_time, x_acceleration, y_acceleration, z_acceleration, height, longitude, latitude) VALUES (?, ?, ?, ?, ?, ?, ?)"
    checkCoordinates = "SELECT entry_time, latitude, longitude FROM sensor_data ORDER BY entry_time DESC LIMIT 1"
    old_coords = [None,None,None]
    connection = sqlite3.connect(dbFolder + dbName)             #connect to database
    cur = connection.cursor()                                   #create cursor to move through database

    try:
       with open(dbFolder + 'schema.sql') as f:                #open database format file
           connection.executescript(f.read())                  #create database tables if not existing
       if fix:                                                 #if there is velocity data (satellite has connection)
           cur.execute(checkCoordinates)
           old_data = cur.fetchall()
           print(old_data[0])
           old_time, old_lat, old_lon = old_data[0]
           print(old_lon)
           if lat == old_lat and lon == old_lon:
               vel = None
               print("Coordinates didn't change since " + old_time)
           cur.execute(logDB_all, (currentTime, x_acc, y_acc, z_acc, vel, height, lon, lat))
       if not fix or vel == None:                              #if there is not velocity data (satellite has no connection)
           cur.execute(logDB_no_vel, (currentTime, x_acc, y_acc, z_acc, height, lon, lat))
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
        "SELECT entry_time, x_acceleration, y_acceleration, z_acceleration, velocity, height FROM \
         ( SELECT entry_time, x_acceleration, y_acceleration, z_acceleration, velocity, height FROM sensor_data \
         ORDER BY entry_time DESC LIMIT " + str(entries) +") \
         ORDER BY entry_time ASC"
    cur.execute(exportScript)                                   #run the export script
    records = cur.fetchall()                                    #get export results

    time = [None for i in range(entries)]
    x_acc = [None for i in range(entries)]
    y_acc = [None for i in range(entries)]
    z_acc = [None for i in range(entries)]
    vel = [None for i in range(entries)]
    height = [None for i in range(entries)]

    for entry, row in enumerate(records):                       #seperate everything into individual sections
        time[entry], x_acc[entry], y_acc[entry], z_acc[entry], vel[entry], height[entry] = row

    return time, x_acc, y_acc, z_acc, vel, height               #return results

#export database to csv file
def exportDB():

    connection = sqlite3.connect(dbFolder + dbName)             #connect to database
    cur = connection.cursor()                                   #create cursor to move through database
    exportScript = \
        "SELECT entry_time, x_acceleration, y_acceleration, z_acceleration, velocity, height \
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