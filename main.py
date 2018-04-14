# #####################################################################################################################
# Project UNDYNE - DEMO 1: Motors go spin... Beholdeth.
# #####################################################################################################################
from motordriver import motordriver
from ltc2990class import ltc2990
from mcp3221class import mcp3221
from bno055class import bno055
from px3class import px3
import flightcontroller

import time
import socket
import sys
s = socket.socket()
address = ('192.168.0.41', 666)
s.bind(address)
print("Awaiting connection to control centre")

s.listen(1)
connection, client = s.accept()
print("Connection raised to: ", client)

imu = bno055()
md = motordriver()
battery = mcp3221()
pid = flightcontroller.pidautopilot()

imu.initalise()
md.pwminit()
currentdemand=[0,0,0,0]
desireddemand=[0,0,0,0]

error_h = 0
error_p = 0
error_r = 0
#control = flightcontroller.pidautopilot()
#PID_heading,PID_pitch, error_h,error_p= control.calculatePID(5, 0)
while(1):
    code = ""
    while(code[-4:] != " ACK"):
        code += connection.recv(16).decode('utf-8')
        if len(code) > 6: code = ""
    # read codes from the command centre and perform actions
    print(code)
    if(code == "SD ACK"):
        # compile message
        print(currentdemand)
        message = "% 0.2f'% 0.2f" %(battery.readadc())
        message += "'% 0.2f" % imu.gettemperature()
        message += "'%0.2f'% 0.2f'% 0.2f" % imu.geteuler()
        message += "'% 0.2f'% 0.2f'% 0.2f" % imu.getmagnetometer()
        message += "'% 0.2f'% 0.2f'% 0.2f" % imu.getgyroscope()
        message += "'% 0.2f'% 0.2f'% 0.2f" % imu.getaccelerometer()
        message += "'% 0.2f'% 0.2f'% 0.2f" % imu.getlinearaccleration()
        message += "'% 0.2f'% 0.2f'% 0.2f'% 0.2f" % imu.getgravity()
        message += "'% 0.2f'% 0.2f'% 0.2f'% 0.2f  ACK" % imu.getgravity()
        connection.sendall(message.encode('utf-8'))
        print("current",currentdemand)

    elif (code == "MD ACK"):
        # compile message and be ready to recieve new instructions
        message = "%s'%s'%s'%s' ACK" %(currentdemand[0], currentdemand[1], currentdemand[2], currentdemand[3])
        print(message)
        connection.sendall(message.encode('utf-8'))
        message = ""
        # Recieve updated demand
        while(message[-4:] != " ACK"):
            message += connection.recv(16).decode('utf-8')
        desireddemand = message.split("'")[:4]
        pidsetpoints = message.split("'")[4:9]
        print(pidsetpoints)
        # heading, roll, pitch, depth, distance
        pidparams = message.split("'")[9:-1]
        print(pidparams)
        desireddemand = list(map(int,  desireddemand))
        pidsetpoints = list(map(float, pidsetpoints))
        pidparams = list(map(float, pidparams))

        print("desired", desireddemand)
        outputheading, outputroll, outputpitch, error_h, error_r, error_p = pid.calculatePID(pidsetpoints[0], pidsetpoints[1], pidsetpoints[2], pidparams, error_h=error_h, error_r=error_r, error_p=error_p)
        print(outputheading, outputroll, outputpitch)
        # Alter RT demand
        desireddemand[0] += int(outputheading)
        # Alter LT demand
        desireddemand[2] -= int(outputheading)
        # Alter RD demand
        desireddemand[1] += int(outputpitch)
        desireddemand[1] += int(outputroll)
        # Alter LD demand
        desireddemand[3] += int(outputpitch)
        desireddemand[3] -= int(outputroll)
        print(desireddemand)
        md.setdemand(desireddemand)
        currentdemand = desireddemand



    elif (code == "DC ACK"):
        md.deactivate()
        s.close()
        break





    #PID_heading, PID_pitch, error_h, error_p= control.calculatePID(10, 0, error_h=error_h, error_p=error_p)
    #print(PID_heading, PID_pitch)
    #time.sleep(1)


