import board
import busio
import adafruit_gps
import adafruit_mpu6050
import adafruit_bmp3xx
import pisugar
from random import random, randint

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
    vel = (gps.speed_knots * 1.15078)

    #altitude in meters based on sea level pressure
    height = bmp.altitude 

    return lateral_acc, vertical_acc, vel, height

def gpsCoordinates():
    return gps.latitude, gps.longitude

def batteryInfo():
    return pisugar.get_battery_level(), pisugar.get_battery_power_plugged()

def oledWrite(recordingStatus):
    if recordingStatus:                                 #get recording status
        recordingText = "Recording"
    else:
        recordingText = "Not Recording"
    bat_percent, charge_status = batteryInfo()          #get battery info
    if charge_status: 
        chargeText = ", Charging"
    else:
        chargeText = ""
    batteryText = "Battery: " + str(bat_percent) + "%" + chargeText
    text = recordingText + "\n" + batteryText           #compile full oled text
    print("Mock OLED Written data:")
    print(text)