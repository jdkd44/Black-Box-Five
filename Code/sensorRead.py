import time
#import board
import busio

import adafruit_gps
import adafruit_mpu6050
import adafruit_bmp3xx

#Creates I2C interface to communicate using pins
#i2c = board.I2C()

#Create a BMP module instance
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

#Create a MPU module instance
#mpu = adafruit_mpu6050.MPU6050(i2c)

#Create a GPS module instance
#gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)

#Initialize GPS module by turning on GGA and RMC info
#gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

#Set update rate to once a second
#gps.send_command(b"PMTK220, 1000") 

#gather sensor data into one location
def dbData():
    #needs some form of logic to return the data that we want logged to database

    
    #TESTING ONLY
    from random import randint
    dataMax = 3
    dataMin = -3    
    lateral_acc = randint(dataMin, dataMax)
    #lateral_acc = mpu.accel_x
    vertical_acc = randint(dataMin, dataMax)
    #vertical_acc = mpu.accel_y
    vel = randint(dataMin, dataMax)
    height = randint(dataMin, dataMax)

    #altitude in meters based on sea level pressure
    #height = bmp.altitude 

    return lateral_acc, vertical_acc, vel, height

def gpsCoordinates():
    #gps_lat = gps.latitude
    #gps_lon = gps.longtidue

    #TESTING ONLY
    from random import randint
    dataMax = 100
    dataMin = -100
    gps_lat = randint(dataMin, dataMax)
    gps_lon = randint(dataMin, dataMax)

    return gps_lat, gps_lon

def batteryInfo():
    #find battery level of the pisugar2 hat

    #TESTING ONLY
    from random import random
    bat_percent = round(random() * 100,2)
    charge_status = False
    return bat_percent, charge_status