from flask import Flask, render_template, jsonify, request, url_for, send_file, redirect
from flask_apscheduler import APScheduler
import datetime
from os import system
from databaseInteract import writeDB, readDB, exportDB, exportFile, exportPath, clearDatabase
from sensorRead import dbData, batteryInfo, gpsData, oledWrite
from time import sleep


#global variables and defaults
dataLogging = False                             #default dataLogging off
timeFormat = "%Y-%m-%d %H:%M:%S.%f"             #formatting for time for database entries - YYYY-MM-DD HH:MM:SS.sss  
shutdownScript = "sudo shutdown now"            #script used to turn device off
pollingRate = 2                                 #times per second to poll the sensors, default 2
oledUpdateInterval = 30                         #seconds between OLED display updates
webPort = 8080                                  #port 80 for http requests


class Config(object):                           #flask scheduler configuration
    SCHEDULER_API_ENABLED = True

def logData():                                  #get data and log it function
    x_acc, y_acc, z_acc, vel, height = dbData()
    currentTime = datetime.datetime.now().strftime(timeFormat)[0:23]
    if writeDB(currentTime, x_acc, y_acc, z_acc, vel, height):
        print("Data has been logged")
    else:
        print("Error in database logging")

def oledUpdate():
    oledWrite(dataLogging)

if __name__ == '__main__':
    app = Flask(__name__)                       #flask app intiation
    app.config.from_object(Config())

    @app.route('/', methods = ['GET','POST'])   #main webpage
    def index():
        if request.method == 'POST':            #if webpage posts data, get the data
            global pollingRate
            global dataLogging
            recordingStatus = request.form['recordingStatus'].upper()
            webPollingRate = float(request.form['pollingRate'])
            if webPollingRate != pollingRate:
                pollingRate = webPollingRate
                scheduler.remove_job(id='logData')
                sleep(2)
                scheduler.add_job(id='logData', func='main:logData', trigger='interval', seconds=(1/webPollingRate), max_instances=1)
            if recordingStatus == "TRUE":
                dataLogging = True
                scheduler.resume_job('logData')
            elif recordingStatus == "FALSE":
                dataLogging = False
                scheduler.pause_job('logData')
            else:
                print("Unexpected Recording Status Returned")
            oledUpdate()
        return render_template("index.html", pollingRate=pollingRate)

    @app.route('/data')                         #send most recent DB entry to webpage
    def data():         
        time, x_acc, y_acc, z_acc, vel, height = readDB()

        x_acc[0], y_acc[0], z_acc[0], vel[0], height[0] = dbData()

        if x_acc > y_acc: lateral_acc = x_acc[0]
        else: lateral_acc = y_acc[0]
        
        return jsonify(
            lateral_acc = lateral_acc,
            vertical_acc = z_acc[0],
            velocity = vel[0],
            height = height[0],
            time = time[0],
            pollingRate = pollingRate
            )

    @app.route('/battery')                      #json for battery status
    def battery():
        bat_percent, charge_status = batteryInfo()
        return jsonify(
            bat_percent = bat_percent,
            charge_status = charge_status
        )

    @app.route('/onload_data')                  #json for javascript initialization
    def onload_data():
        return jsonify(
            recordingStatus = dataLogging
        )

    @app.route('/gps')
    def gps():
        longitude, latitude, fix = gpsData()
        if fix: 
            gps_lat = latitude
            gps_lon = longitude
        else:
            gps_lat = "NULL"
            gps_lon = "NULL"
        return jsonify(
            gps_lat = gps_lat,
            gps_lon = gps_lon,
            fix = fix
        )

    @app.route('/download')                     #csv export file download
    def download():
        exportDB()
        return send_file(exportPath + exportFile, as_attachment=True)

    @app.route('/cleardb', methods=['POST'])    #delete or clear database
    def clearDB():
        if request.method == 'POST':
            if request.form['clear_confirmation']:
                print("clearing database")
                clearDatabase()
            else:
                print("database not cleared")
        return ('', 204)
    
    @app.route('/shutdown', methods=['POST'])   #shutdown blackbox
    def shutdown():
        if request.method == 'POST':
            if request.form['shutdown_confirmation']:
                system(shutdownScript) 
        return ('', 204)

    @app.errorhandler(404)                      #unknown path
    def page_not_found(e):
        return redirect(url_for('index')), 404

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id='logData', func='main:logData', trigger='interval', seconds=(1/pollingRate), max_instances=1)
#    scheduler.add_job(id='oledUpdate', func='main:oledUpdate', trigger='interval', seconds=oledUpdateInterval, max_instances=1)
    if not dataLogging:
        scheduler.pause_job('logData')
    app.run(host="0.0.0.0",port=webPort)         #start flask server
