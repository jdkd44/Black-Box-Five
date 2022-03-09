import board
import busio
import adafruit_gps
import adafruit_mpu6050
import adafruit_bmp3xx
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
mpu = adafruit_mpu6050.MPU6050(i2c)
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)

#Initialize GPS module by turning on GGA and RMC info
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

#Set update rate to once a second
gps.send_command(b"PMTK220, 1000") 

#gather sensor data into one location
def dbData():
    #needs some form of logic to return the data that we want logged to database
    lateral_acc = mpu.accel_x
    vertical_acc = mpu.accel_y

    #altitude in meters based on sea level pressure
    height = bmp.altitude 

    return lateral_acc, vertical_acc, vel, height

def gpsCoordinates():
    gps_lat = gps.latitude
    gps_lon = gps.longtidue

    return gps_lat, gps_lon

def batteryInfo():
    #TESTING ONLY
    from random import random
    bat_percent = round(random() * 100,2)
    charge_status = False
    return bat_percent, charge_status 

# def oledWrite(recordingStatus):
#     oled.fill(0)    #clear display
#     oled.show()
#     image = Image.new("1", (oled.width, oled.height))   #make an image object
#     draw = ImageDraw.Draw(image)                        #make a drawing object to write on the image
#     font = ImageFont.load_default()                     #load the default font
    
#     if recordingStatus:                                 #get recording status
#         recordingText = "Recording"
#     else:
#         recordingText = "Not Recording"
#     bat_percent, charge_status = batteryInfo()          #get battery info
#     if charge_status: 
#         chargeText = ", Charging"
#     else:
#         chargeText = ""
#     batteryText = "Battery: " + str(bat_percent) + "%" + chargeText
#     text = recordingText + "\n" + chargeText            #compile full oled text

#     (font_width, font_height) = font.getsize(text)
#     draw.text(
#         (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
#         text,
#         font=font,
#         fill=255,
#     )
#     oled.image(image)                                   #create image
#     oled.show()                                         #display image
