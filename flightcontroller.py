# #####################################################################################################################
# Project UNDYNE - MODULE 6: The one ring rule them all...
# #####################################################################################################################

# 'Flight' controller for UNDYNE, composed of various control methods namely: Heading and Pitch based motor control, as
# well as Depth based motor control (TBA)
# PID control implemented for Heading, Pitch and Roll. All seems to be working pretty good. Deadband of +-2% to prevent
# motors from wanting to die. Pressure still needs implemented.

# PID control decoupled, from the X, Y, Z
# Heading should be added to RT and subtracted from LT
# Pitch should be added to RD and LD
# Roll should be added to RD and subtracted from LT
# Depth should be added to RD and LD
#            |  |
#            |  |
#            |  |
#            |  |
#            |  |

from bno055class import bno055
from motordriver import motordriver
import time
md = motordriver()
imu = bno055()
# motordriver still needs init'ed in the main programme...
deadband = 2

class emergency():
    def start(self):
        md.setdemand([4095, 0, 4095, 0])
        time.sleep(10)
        raise RuntimeError("Emergency surface... HELP. PLEASE.")

class standby():
    def start(self):
        md.deactivate()
    def end(self):
        md.initialise()

class pidautopilot():
    def __init__(self):
        self.maxdemand = 200

        self.Kp_Heading = 1
        self.Ki_Heading = 0
        self.Kd_Heading = 0

        self.Heading_Setpoint = 0
        self.headingerror = 0
        self.lastheading = 0
        self.imember_h = 0

        self.Kp_Pitch = 1
        self.Ki_Pitch = 0
        self.Kd_Pitch = 0

        self.pitchsetpoint = 0
        self.pitcherror = 0
        self.lastpitch = 0
        self.imember_p = 0

        self.Kp_Roll = 1
        self.Ki_Roll = 0
        self.Kd_Roll = 0

        self.rollsetpoint = 0
        self.rollerror = 0
        self.lastroll = 0
        self.imember_r = 0

        self.Kp_depth = 1
        self.Ki_depth = 0
        self.Kd_depth = 0

        self.depthsetpoint = 0
        self.deptherror = 0
        self.lastdepth = 0
        self.imember_dph = 0

    def calculatePID(self, setpoint_h, setpoint_p, setpoint_r, K, error_h=0, error_p=0, error_r=0):
        headingoutput, error1 = self.headingPID(setpoint_h, K, error=error_h)
        rolloutput, error3 = self.rollPID(setpoint_r, K, error=error_r)
        pitchoutput, error2 = self.pitchPID(setpoint_p, K, error=error_p)

        #print(headingoutput)
        return headingoutput, rolloutput, pitchoutput, error1, error2, error3

    def headingPID(self, setpoint, K, error=0):
        self.Kp_Heading = K[0]
        self.Ki_Heading = K[1]
        self.Kd_Heading = K[2]

        heading = imu.geteuler()[0]
        self.Heading_Setpoint = setpoint
        self.headingerror = error
        # convert heading from 0:360 to -180:180
        if heading > 180:
            heading -= 360
        temperror = self.Heading_Setpoint - heading
        # Ensure the integral member is not in excess of the maximum demand
        self.imember_h += self.Ki_Heading * temperror
        if self.imember_h > self.maxdemand: self.imember_h = self.maxdemand
        elif self.imember_h < -1*self.maxdemand: self.imember_h = -1*self.maxdemand

        output = (self.Kp_Heading * temperror) + self.imember_h + (self.Kd_Heading * (temperror - self.headingerror))
        # Ensure output does not exceed maximum
        if output > self.maxdemand: output = self.maxdemand
        elif output < -1*self.maxdemand: output = -1*self.maxdemand
        # Add a slight deadband... The motors will thank you later.
        elif output > -1*deadband and output < deadband:
            output = 0
        self.headingerror = temperror
        return output, self.headingerror

    def pitchPID(self, setpoint, K, error=0):
        self.Kp_Pitch = K[3]
        self.Ki_Pitch = K[4]
        self.Kd_Pitch = K[5]

        pitch = imu.geteuler()[2]
        print(pitch)
        self.pitchsetpoint = setpoint
        self.pitcherror = error

        temperror = self.pitchsetpoint - pitch
        # Ensure the integral member is not in excess of the maximum demand
        self.imember_p += self.Ki_Pitch * temperror
        if self.imember_p > self.maxdemand:
            self.imember_p = self.maxdemand
        elif self.imember_p < -1 * self.maxdemand:
            self.imember_p = -1 * self.maxdemand

        output = (self.Kp_Pitch * temperror) + self.imember_p + (self.Kd_Pitch * (temperror - self.pitcherror))
        # Ensure output does not exceed maximum
        if output > self.maxdemand:
            output = self.maxdemand
        elif output < -1 * self.maxdemand:
            output = -1 * self.maxdemand
        # Add a slight deadband... The motors will thank you later.
        elif output > -1*deadband and output < deadband:
            output = 0
        self.pitcherror = temperror
        return output, self.pitcherror

    def rollPID(self, setpoint, K, error=0):
        self.Kp_Roll = K[6]
        self.Ki_Roll = K[7]
        self.Kd_Roll = K[8]

        roll = imu.geteuler()[1]
        print(roll)
        self.rollsetpoint = setpoint
        self.rollerror = error

        temperror = self.rollsetpoint - roll
        # Ensure the integral member is not in excess of the maximum demand
        self.imember_r += self.Ki_Roll * temperror
        if self.imember_r > self.maxdemand:
            self.imember_r = self.maxdemand
        elif self.imember_r < -1 * self.maxdemand:
            self.imember_r = -1 * self.maxdemand

        output = (self.Kp_Roll * temperror) + self.imember_r + (self.Kd_Roll * (temperror - self.rollerror))
        # Ensure output does not exceed maximum
        if output > self.maxdemand:
            output = self.maxdemand
        elif output < -1 * self.maxdemand:
            output = -1 * self.maxdemand
        # Add a slight deadband... The motors will thank you later.
        elif output > -1*deadband and output < deadband:
            output = 0
        self.rollerror = temperror
        return output, self.rollerror













