import random
from databaseInteract import clearDatabase, writeDB
from sensorRead import dbData

#Generates new random data points and inserts into database
#Wipes all current database entries

dataPoints = 100 #dont go more than 1000, messes up date formatting
dataMax = 3
dataMin = -3

clearDatabase()
for i in range(dataPoints):
    lateral_acc, vertical_acc, vel, height = dbData()
    writeDB("2022-03-01 01:02:"str(i).zfill(2)+".000", lateral_acc, vertical_acc, vel, height)
