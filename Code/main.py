from flask import Flask, render_template, jsonify, request, url_for, send_file, redirect
from databaseInteract import writeDB, readDB, exportDB, exportFile, exportPath, clearDatabase
from sensorRead import dbData, batteryInfo, gpsCoordinates
import datetime


#variables
webUI = True                        #default webUI on
dataLogging = False                 #default dataLogging off
timeFormat = "%Y-%m-%d %H:%M:%S.%f" #formatting for time for database entries - YYYY-MM-DD HH:MM:SS.sss  
pollingRate = 2                     #times per second to poll the sensors, default 2
webPort = 80                        #port 80 for http requests

#flask app intiation
app = Flask(__name__)

#flask stuff
@app.route('/', methods = ['GET','POST'])  #main webpage
def index():
    if request.method == 'POST':
        global dataLogging
        recordingStatus = request.form['recordingStatus'].upper()
        if recordingStatus == "TRUE":
            dataLogging = True
        elif recordingStatus == "FALSE":
            dataLogging = False
        else:
            print("Unexpected Data Returned")
    return render_template("index.html", pollingRate=pollingRate)

@app.route('/data')         #get current data and log to database
def data():         
    lateral_acc, vertical_acc, vel, height = dbData()
    gps_lat, gps_lon = gpsCoordinates()
    currentTime = datetime.datetime.now().strftime(timeFormat)[0:23]
    #writeDB(currentTime.strftime(timeFormat), lateral_acc, vertical_acc, vel, height)
    
    return jsonify(
        lateral_acc = lateral_acc,
        vertical_acc = vertical_acc,
        velocity = vel,
        height = height,
        gps_lat = gps_lat,
        gps_lon = gps_lon,
        time = currentTime,
        pollingRate = pollingRate
        )

@app.route('/battery')      #json for battery status
def battery():
    bat_percent, charge_status = batteryInfo()
    return jsonify(
        bat_percent = bat_percent,
        charge_status = charge_status
    )

@app.route('/onload_data')  #json for javascript initialization
def onload_data():
    return jsonify(
        recordingStatus = dataLogging
    )

@app.route('/download')     #csv export file download
def download():
    exportDB()
    return send_file(exportPath + exportFile, as_attachment=True)

@app.route('/cleardb', methods=['POST'])
def clearDB():
    if request.method == 'POST':
        if request.form['clear_confirmation']:
            clearDatabase()
    return ('', 204)

@app.errorhandler(404)      #unknown path
def page_not_found(e):
    return redirect(url_for('index')), 404

#if webUI true, start webserver
if webUI:
    app.run(debug=True, port=webPort)

#NEEDS LOGIC TO STOP RUNNING WHEN CONDITIONS ARE MET (PHYSICAL BUTTON START/STOP)
#NEEDS LOGIC TO CHOOSE TO CLEAR DATABASE
#NEEDS LOGIC TO SHUTDOWN WEBSITE
#NEEDS OLED SCREEN CONTROL TO DISPLAY WEBPAGE/RECORDING STATUS
#NEEDS LOGIC TO START/STOP DATA RECORDING

