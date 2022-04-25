import board
import busio
import adafruit_gps
import adafruit_mpu6050
import adafruit_bmp3xx
from random import random, randint

from pisugar import PiSugarServer, connect_tcp

dataMin = -3
dataMax = 3

# import adafruit_ssd1306     #oled module -> #pi OLED setup:  https://learn.adafruit.com/monochrome-oled-breakouts/python-setup
# from PIL import Image, ImageDraw, ImageFont #library from installing a python image thing once on the pi

# #variables
# oledW = 128
# oledH = 64
# oledAddr = 0x78

#Creates I2C interface to communicate using pins
i2c = busio.I2C(board.SCL, board.SDA)

#create opjects for itnerfacing with sensors
# oled = adafruit_ssd1306.SSD1306_I2C(oledW, oledH, i2c, addr=oledAddr)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
#mpu = adafruit_mpu6050.MPU6050(i2c)
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)

conn, event_conn =  connect_tcp()
batteryServer = PiSugarServer(conn,event_conn)

#Initialize GPS module by turning on GGA and RMC info
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

#Set update rate to once a second
gps.send_command(b"PMTK220, 1000")

#gather sensor data into one location
def dbData():
    #needs some form of logic to return the data that we want logged to database
    lateral_acc = randint(dataMin, dataMax)
    vertical_acc = randint(dataMin, dataMax)

    #convert speed in knots to mph
    if gps.speed_knots is not None: vel = round(gps.speed_knots * 1.15078,3)
    else: vel = "NULL"

    #altitude in meters based on sea level pressure
    height = bmp.altitude

    return lateral_acc, vertical_acc, vel, height

def gpsCoordinates():
    if (gps.latitude is not None) and (gps.longitude is not None): return gps.latitude, gps.longitude
    else: return "NULL", "NULL"

def batteryInfo():
    if batteryServer.get_battery_power_plugged():
        charge_status = "Charging"
    elif not batteryServer.get_battery_power_plugged():
        charge_status = "Discharging"
    else:
        charge_status = "Unable to get charging status"
    return round(batteryServer.get_battery_level(), 2), charge_status

def oledWrite(recordingStatus):
    if recordingStatus:                                 #get recording status
        recordingText = "Recording"
    else:
        recordingText = "Not Recording"
    bat_percent, charge_status = batteryInfo()          #get battery info
    batteryText = "Battery: " + str(bat_percent) + "%" + charge_status
    text = recordingText + "\n" + batteryText           #compile full oled text
    print("Mock OLED Written data:")
    print(text)
