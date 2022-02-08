import sqlite3
import time

dbName = 'BlackBox.db'
sampleFrequency = 0.5   #time between samples in seconds, needs integrated into flask webpage

def getSensData():
    #get that data
    return lateral_acc, vertical_acc, vel, height

def clearDatabase():
    connection = sqlite3.connect(dbName)                        #connect to database
    cur = connection.cursor()                                   #create cursor to move through database
    with open('dbclear.sql') as f:                              #open database format file
        connection.executescript(f.read())                      #create database tables if not existing
    connection.commit()                                         #commit database changes
    connection.close()                                          #close database connection

def logData(currentTime, lateral_acc, vertical_acc, vel, height):                               #FOR FINAL CODE MAKE TIME GENERATED IN THIS FUNCTION
#    currentTime = datetime('now')                               #get current time
    connection = sqlite3.connect(dbName)                        #connect to database
    cur = connection.cursor()                                   #create cursor to move through database
    with open('schema.sql') as f:                               #open database format file
        connection.executescript(f.read())                      #create database tables if not existing

    #sample data logging
    cur.execute("INSERT INTO acc_data (time, lateral_acc, vertical_acc) VALUES (?, ?, ?)",(currentTime, lateral_acc, vertical_acc))
    cur.execute("INSERT INTO vel_data (time, vel) VALUES (?, ?)",(currentTime, vel))    
    cur.execute("INSERT INTO alt_data (time, height) VALUES (?, ?)",(currentTime, height))    

    connection.commit()                                         #commit database changes
    connection.close()                                          #close database connection

#TESTING ONLY - GENERATES RANDOM SENSOR DATA, wipes database every time
import random
dataPoints = 1000
dataMax = 3
dataMin = -3
startUnixTime = 1641016800
clearDatabase()
for i in range(startUnixTime, startUnixTime + dataPoints):
    lateral_acc = random.randint(dataMin, dataMax)
    vertical_acc = random.randint(dataMin, dataMax)
    vel = random.randint(dataMin, dataMax)
    height = random.randint(dataMin, dataMax)
    logData(i, lateral_acc, vertical_acc, vel, height)

    

#run = 1                                                         #NEEDS LOGIC TO STOP RUNNING WHEN CONDITIONS ARE MET
#                                                                #ALSO NEEDS LOGIC TO CHOOSE TO CLEAR DATABASE
#
#
#while(run):                                                     #main program loop
#    lateral_acc, vertical_acc, vel, height = getSensData()      #get sensor data
#    logData(lateral_acc, vertical_acc, vel, height)             #log data
#    time.sleep(sampleFrequency)                                 #wait for specified amount of time
