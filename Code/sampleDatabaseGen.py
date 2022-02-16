import random
import databaseInteract

#Generates new random data points and inserts into database
#Wipes all current database entries

dataPoints = 999
dataMax = 3
dataMin = -3

dataclearDatabase()
for i in range(dataPoints):
    lateral_acc = random.randint(dataMin, dataMax)
    vertical_acc = random.randint(dataMin, dataMax)
    vel = random.randint(dataMin, dataMax)
    height = random.randint(dataMin, dataMax)
    logData("0000-00-00 00:00:00."+str(i), lateral_acc, vertical_acc, vel, height)