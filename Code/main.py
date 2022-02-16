from flask import Flask, render_template, jsonify
from databaseInteract import logData
from sensorRead import dbData
import datetime
import time


#variables
webUI = True            #default webUI on
dataLogging = False     #default dataLogging off
sampleFrequency = 0.5   #default to 0.5sec, allow updates via webpage
webPort = 80            #port 80 for http requests

#flask app intiation
app = Flask(__name__)

#main webpage
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/data')
def data():         #datastream for logging data using intercooler.js
    lateral_acc, vertical_acc, vel, height = dbData()
    return jsonify(
        lateral_acc = lateral_acc,
        vertical_acc = vertical_acc,
        velocity = vel,
        height = height
        )

#if webUI true, start webserver
if webUI:
    app.run(debug=True, port=webPort)

                                                                    #NEEDS LOGIC TO STOP RUNNING WHEN CONDITIONS ARE MET
                                                                    #NEEDS LOGIC TO CHOOSE TO CLEAR DATABASE
                                                                    #NEEDS LOGIC TO SHUTDOWN WEBSITE
                                                                    #NEEDS OLED SCREEN CONTROL TO DISPLAY WEBPAGE/RECORDING STATUS


while(dataLogging):                                                 #if dataLogging true, record sensor data
    lateral_acc, vertical_acc, vel, height = dbData()               #get sensor data
    currentTime = datetime.datetime.now()
    logData(currentTime.strftime("%Y-%m-%d %H:%M:%S.%L"), lateral_acc, vertical_acc, vel, height)             #log data
    time.sleep(sampleFrequency)                                     #wait for specified amount of time
