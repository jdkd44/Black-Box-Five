from flask import Flask, render_template, jsonify, request, url_for, send_file, redirect
from databaseInteract import writeDB, readDB, exportDB, exportFile, exportPath
from sensorRead import dbData, batteryInfo, gpsCoordinates
import datetime


#variables
webUI = True                        #default webUI on
dataLogging = False                 #default dataLogging off
timeFormat = "%Y-%m-%d %H:%M:%S.%L" #formatting for time for database entries - YYYY-MM-DD HH:MM:SS.sss  
pollingRate = 2                     #times per second to poll the sensors, default 2
webPort = 80                        #port 80 for http requests


#flask app intiation
app = Flask(__name__)

#main webpage
@app.route('/', methods = ['POST', 'GET'])
def index():
    if not dataLogging: recordingButton = "Start Recording"
    else: recordingButton = "Stop Recording"

    if request.method == 'POST':
        if request.form['recordButton']: toggleDataLogging()
    return render_template("index.html", recordingButton=recordingButton, pollingRate=pollingRate)

@app.route('/data')         #json for current data
def data():         
    lateral_acc, vertical_acc, vel, height = dbData()
    gps_lat, gps_lon = gpsCoordinates()
    bat_percent, charge_status = batteryInfo()
    return jsonify(
        lateral_acc = lateral_acc,
        vertical_acc = vertical_acc,
        velocity = vel,
        height = height,
        gps_lat = gps_lat,
        gps_lon = gps_lon,
        bat_percent = bat_percent,
        charge_status = charge_status,
        time = datetime.datetime.now()
        )

@app.route('/chart')        #json for past database entries
def chart():
    time, lateral_acc, vertical_acc, vel, height = readDB()
    return jsonify(
        time = time,
        lateral_acc = lateral_acc,
        vertical_acc = vertical_acc,
        velocity = vel,
        height = height
    )

@app.route('/download')     #csv export file download
def download():
    exportDB()
    return send_file(exportPath + exportFile, as_attachment=True)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404


def toggleDataLogging():
    dataLogging = not dataLogging

#log data function
def logData():
    lateral_acc, vertical_acc, vel, height = dbData()                                   #get sensor data
    currentTime = datetime.datetime.now()                                               #get current time
    writeDB(currentTime.strftime(timeFormat), lateral_acc, vertical_acc, vel, height)   #log data

#if webUI true, start webserver
if webUI:
    app.run(debug=True, port=webPort)

#NEEDS LOGIC TO STOP RUNNING WHEN CONDITIONS ARE MET (PHYSICAL BUTTON START/STOP)
#NEEDS LOGIC TO CHOOSE TO CLEAR DATABASE
#NEEDS LOGIC TO SHUTDOWN WEBSITE
#NEEDS OLED SCREEN CONTROL TO DISPLAY WEBPAGE/RECORDING STATUS
#NEEDS LOGIC TO START/STOP DATA RECORDING

