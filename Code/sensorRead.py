
#gather sensor data into one location
def dbData():
    #needs some form of logic to return the data that we want logged to database

    
    #TESTING ONLY
    from random import randint
    dataMax = 3
    dataMin = -3    
    lateral_acc = randint(dataMin, dataMax)
    vertical_acc = randint(dataMin, dataMax)
    vel = randint(dataMin, dataMax)
    height = randint(dataMin, dataMax)

    return lateral_acc, vertical_acc, vel, height

def gpsCoordinates():

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