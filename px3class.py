# #####################################################################################################################
# Project UNDYNE - MODULE 4
# #####################################################################################################################

# Drivers for the Honeywell PX3 pressure sensor, utilising predefined drivers for the ITC2990 ADC

from ltc2990class import ltc2990
from bno055class import bno055

adc4 = ltc2990()
imu = bno055()

# Measured in bars and voltage
minpressure = [0, 0.5]
maxpressure = [25, 4.5]

voltagerange  = maxpressure[1] - minpressure[1]
pressurerange = maxpressure[0] - minpressure[0]

pervoltage = pressurerange / voltagerange # 6.25 bar per 1 voltage increase

class px3():
    def pressure(self):
        voltage, temp = adc4.pressure()
        # Voltage divider will be used... ltc2990 cannot exceed 3.3V analogue input
        voltage = (2*voltage)
        pressure = voltage*pervoltage
        print("%s Bars, at %s Celsius" % (pressure, temp))
        return pressure, temp

    def simpledepth(self):
        bars, temp = self.pressure()
        depth = bars * 1.019716
        print("Depth: %s m" % depth)
        return depth

    def complexdepth(self):
        # More sophistcated method which accounts for compressity of water due to gravity
        # Proves more accurate at greater depth
        bars, temp = self.pressure()
        gravity = imu.getgravity()
        c1, c2, c3, c4 = -1.82*pow(10, -15), 2.279*pow(10,-10), -2.512*pow(10, -5), 9.72659
        # The following formula return depth in meters
        depth = ((c1*(bars + c2))*(bars - c3)*(bars + c4)*bars)/gravity
        print("Depth: %s m" % depth)
        return depth






