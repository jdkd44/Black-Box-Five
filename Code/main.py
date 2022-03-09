from flask import Flask, render_template, jsonify, request, url_for, send_file, redirect
from flask_apscheduler import APScheduler
import datetime
from os import system
from databaseInteract import writeDB, readDB, exportDB, exportFile, exportPath, clearDatabase
from sensorRead import dbData, batteryInfo, gpsCoordinates


#global variables and defaults
dataLogging = False                             #default dataLogging off
timeFormat = "%Y-%m-%d %H:%M:%S.%f"             #formatting for time for database entries - YYYY-MM-DD HH:MM:SS.sss  
shutdownScript = "sudo shutdown now"            #script used to turn device off
pollingRate = 2                                 #times per second to poll the sensors, default 2
webPort = 80                                    #port 80 for http requests


class Config(object):                           #flask scheduler configuration
    SCHEDULER_API_ENABLED = True

def logData():                                  #get data and log it function
    lateral_acc, vertical_acc, vel, height = dbData()
    currentTime = datetime.datetime.now().strftime(timeFormat)[0:23]
    if writeDB(currentTime, lateral_acc, vertical_acc, vel, height):
        print("Data has been logged")
    else:
        print("Error in database logging")
    
if __name__ == '__main__':
    app = Flask(__name__)                       #flask app intiation
    app.config.from_object(Config())

    @app.route('/', methods = ['GET','POST'])   #main webpage
    def index():
        if request.method == 'POST':            #if webpage posts data, get the data
            global dataLogging
            global pollingRate

            recordingStatus = request.form['recordingStatus'].upper()
            webPollingRate = float(request.form['pollingRate'])
            if webPollingRate != pollingRate:
                pollingRate = webPollingRate
                scheduler.remove_job(id='logData')
                scheduler.add_job(id='logData', func='main:logData', trigger='interval', seconds=(1/webPollingRate), max_instances=1)
                print('seconds: '+str(1/webPollingRate))
                print('scheduler: '+str(scheduler.get_job(id='logData')))
            if recordingStatus == "TRUE":
                dataLogging = True
                scheduler.resume()
            elif recordingStatus == "FALSE":
                dataLogging = False
                scheduler.pause()
            else:
                print("Unexpected Recording Status Returned")

        return render_template("index.html", pollingRate=pollingRate)

    @app.route('/data')             #send most recent DB entry to webpage
    def data():         
        time, lateral_acc, vertical_acc, vel, height = readDB()
        gps_lat, gps_lon = gpsCoordinates()

        return jsonify(
            lateral_acc = lateral_acc[0],
            vertical_acc = vertical_acc[0],
            velocity = vel[0],
            height = height[0],
            time = time[0],
            gps_lat = gps_lat,
            gps_lon = gps_lon,
            pollingRate = pollingRate
            )

    @app.route('/battery')          #json for battery status
    def battery():
        bat_percent, charge_status = batteryInfo()
        return jsonify(
            bat_percent = bat_percent,
            charge_status = charge_status
        )

    @app.route('/onload_data')      #json for javascript initialization
    def onload_data():
        return jsonify(
            recordingStatus = dataLogging
        )

    @app.route('/download')         #csv export file download
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
    scheduler.start(paused=(not dataLogging))
    scheduler.add_job(id='logData', func='main:logData', trigger='interval', seconds=(1/pollingRate), max_instances=1)
    app.run(port=webPort)                       #start flask server

#NEEDS LOGIC TO STOP RUNNING WHEN CONDITIONS ARE MET (PHYSICAL BUTTON START/STOP)
#NEEDS LOGIC TO SHUTDOWN WEBSITE
#NEEDS OLED SCREEN CONTROL TO DISPLAY WEBPAGE/RECORDING STATUS
