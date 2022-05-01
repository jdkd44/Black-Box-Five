import board
import busio
import adafruit_gps
import adafruit_mpu6050
import adafruit_bmp3xx
from pisugar import PiSugarServer, connect_tcp


# import adafruit_ssd1306     #oled module -> #pi OLED setup:  https://learn.adafruit.com/monochrome-oled-breakouts/python-setup
# from PIL import Image, ImageDraw, ImageFont #library from installing a python image thing once on the pi

# #variables
oledW = 128
oledH = 64
oledAddr = 0x3c

#Creates I2C interface to communicate using pins
i2c = busio.I2C(board.SCL, board.SDA)

#create opjects for itnerfacing with sensors
# oled = adafruit_ssd1306.SSD1306_I2C(oledW, oledH, i2c, addr=oledAddr)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
mpu = adafruit_mpu6050.MPU6050(i2c)
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)

conn, event_conn =  connect_tcp()
batteryServer = PiSugarServer(conn,event_conn)

#Initialize GPS module by turning on GGA and RMC info
gps.send_command(b"PMTK314,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,0")

#Set update rate to once a second
gps.send_command(b"PMTK220, 1000")

#gather sensor data into one location
def dbData():
    gps.update()
    acc = mpu.acceleration              #get acceleration
    x_acc = round(acc[0] / 9.8, 3)      #convert to G's and round to 3 decimal points
    y_acc = round(acc[1] / 9.8, 3)
    z_acc = round((acc[2] + 9.8) / 9.8, 3)
    if gps.has_fix:                     #get velocity if GPS has a fix
        print(gps.speed_knots)
        if gps.speed_knots is not None: 
            vel = round(gps.speed_knots * 1.15078,3)
            print(vel)
        else: vel = "INVALID GPS DATA" 
    else: vel = "NO GPS FIX"
    height = round(bmp.altitude * 3.28084, 3)   #get altitude based on pressure and ocnvert to ft

    return x_acc, y_acc, z_acc, vel, height

def gpsData():                          #get gps data (lon, lat, and fix status)
    gps.update()
    return gps.longitude, gps.latitude, gps.has_fix

def batteryInfo():                      #get battery info
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
    batteryText = "Battery: " + str(bat_percent) + "% | " + str(charge_status)
    text = recordingText + "\n" + batteryText           #compile full oled text
    print("Mock OLED Written data:")
    print(text)

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