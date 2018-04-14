# #####################################################################################################################
# Project UNDYNE - DEMO 2: Here lies an aboundance of sensor readings.
# #####################################################################################################################
from bno055class import bno055
from ltc2990class import ltc2990
from mcp3221class import mcp3221
from Server import server
import time
#from px3class import px3
# Make a UDP socket to transfer some data...

TCP = server()
TCP.connect()

starttime = time.time()
print("Welcome to the UNDYNE sensor suite... Brace yourself for many numbers")
print("")
imu = bno055()
adc = ltc2990()
vbatt = mcp3221()

imu.initalise()
currentposition, currentvelocity, currenttime = imu.getposition(starttime)
adc.initadc()
# Read the battery voltage and per cell voltage
print("Firstly, the single channel ADC")
BATT, CELL = vbatt.readadc()
print("Battery Voltage: %0.2f" % BATT)
print("Cell Voltage   : %0.2f" % CELL)
print("")
message = "%0.2f'%0.2f" %(BATT, CELL)
TCP.senddata(message)





# Read the ADC and display it's goodies
print("Secondly, the four channel ADC")
adc.readadc()
print("")
message = "% 0.2f" %imu.gettemperature()
message += "'%0.2f'% 0.2f'% 0.2f" % imu.geteuler()
message += "'% 0.2f'% 0.2f'% 0.2f" % imu.getmagnetometer()
message += "'% 0.2f'% 0.2f'% 0.2f" % imu.getgyroscope()
message += "'% 0.2f'% 0.2f'% 0.2f" % imu.getaccelerometer()
message += "'% 0.2f'% 0.2f'% 0.2f" % imu.getlinearaccleration()
message += "'% 0.2f'% 0.2f'% 0.2f'% 0.2f" % imu.getgravity()
message += "'% 0.2f'% 0.2f'% 0.2f'% 0.2f" % imu.getgravity()
print(message)
time.sleep(1)
TCP.senddata(message)

# Read the NDOF sensor suite
print("Thirdly, the sensor suite native to the IMU")
print("Temperature          | %0.2f Celsius" % imu.gettemperature())
print("")
print("Euler Angle          | Heading: %0.2f  Pitch: %0.2f  Role: %0.2f" % imu.geteuler())
print("")
print("                         X      Y      Z     W")
print("Magnetometer         | % 0.2f % 0.2f % 0.2f" % imu.getmagnetometer())
print("")
print("Angular Velocity     | % 0.2f  % 0.2f  % 0.2f" % imu.getgyroscope())
print("")
print("Accelerometer        | % 0.2f  % 0.2f % 0.2f" % imu.getaccelerometer())
print("")
print("Linear Accleration   | % 0.2f  % 0.2f  % 0.2f" % imu.getlinearaccleration())
print("")
print("Gravity:    %0.2f     | % 0.2f  % 0.2f  % 0.2f" % imu.getgravity())
print("")
print("Absolute Orienation  | % 0.2f  % 0.2f  % 0.2f % 0.2f" % imu.getquaternion())
print("")

# Reawd PX3 sensor...
TCP.disconnect()
print("Lastly, time for some... Less accurate readings...")
print("Press CTRL+C at any time, to end")
while(1):
    currentposition, currentvelocity, currenttime = imu.getposition(previoustime=currenttime, previousposition=currentposition, previousvelocity=currentvelocity)
    print("Current Position: % 0.2f" %currentposition)
    print("Current Velocity: % 0.2f" %currentvelocity)
    time.sleep(2)
    if (currentposition > 0.1 or currentposition < -0.1):
        raise RuntimeError("Error: How has the sensor moved?")








