import random
from databaseInteract import clearDatabase, logData

#Generates new random data points and inserts into database
#Wipes all current database entries

dataPoints = 1000 #dont go more than 1000, messes up date formatting
dataMax = 3
dataMin = -3

clearDatabase()
for i in range(dataPoints):
    lateral_acc = random.randint(dataMin, dataMax)
    vertical_acc = random.randint(dataMin, dataMax)
    vel = random.randint(dataMin, dataMax)
    height = random.randint(dataMin, dataMax)
    logData("0000-00-00 00:00:00."+str(i).zfill(3), lateral_acc, vertical_acc, vel, height)