
#gather sensor data into one location
def dbData():
    #needs some form of logic to return the data that we want logged to database
    return lateral_acc, vertical_acc, vel, height

def batteryInfo():
    #find battery level of the pisugar2 hat
    return bat_percent, charge_status