from flask import Flask, render_template, request
import sqlite3
import time

#variables
dbName = 'BlackBox.db'
webUI = True            #default webUI on
sampleFrequency = 0.5   #default to 0.5sec, allow updates via webpage


app = Flask(__name__)

#main webpage
@app.route('/')
def index():
    return render_template("index.html")

#gather sensor data
def getSensData():
    #get that data
    return lateral_acc, vertical_acc, vel, height

#completely wipe database
def clearDatabase():
    connection = sqlite3.connect(dbName)                        #connect to database
    cur = connection.cursor()                                   #create cursor to move through database
    with open('dbclear.sql') as f:                              #open database format file
        connection.executescript(f.read())                      #create database tables if not existing
    connection.commit()                                         #commit database changes
    connection.close()                                          #close database connection

#write sensor data into database                                #WHILE DATABASE OPEN, READ CONTENTS AND PASS INTO WEBPAGE IF WEBSERVER RUNNING
def logData(lateral_acc, vertical_acc, vel, height):
    currentTime = datetime('now')                               #get current time
    connection = sqlite3.connect(dbName)                        #connect to database
    cur = connection.cursor()                                   #create cursor to move through database
    with open('schema.sql') as f:                               #open database format file
        connection.executescript(f.read())                      #create database tables if not existing

    if webUI:
        #get database history and pass into webpage for chart updates
    
    #data logging
    cur.execute("INSERT INTO acc_data (time, lateral_acc, vertical_acc) VALUES (?, ?, ?)",(lateral_acc, vertical_acc))
    cur.execute("INSERT INTO vel_data (time, vel) VALUES (?, ?)",(vel))    
    cur.execute("INSERT INTO alt_data (time, height) VALUES (?, ?)",(height))    

    connection.commit()                                         #commit database changes
    connection.close()                                          #close database connection

#if webUI, start webserver
if webUI:
    app.run(debug=True, port=80)

                                                                #NEEDS LOGIC TO STOP RUNNING WHEN CONDITIONS ARE MET
                                                                #NEEDS LOGIC TO CHOOSE TO CLEAR DATABASE
                                                                #NEEDS LOGIC TO SHUTDOWN WEBSITE
                                                                #NEEDS OLED SCREEN CONTROL TO DISPLAY WEBPAGE/RECORDING STATUS

logData = False
while(logData):                                                 #main program loop
    lateral_acc, vertical_acc, vel, height = getSensData()      #get sensor data
    logData(lateral_acc, vertical_acc, vel, height)             #log data
    time.sleep(sampleFrequency)                                 #wait for specified amount of time
