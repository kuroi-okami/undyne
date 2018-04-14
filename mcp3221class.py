# #####################################################################################################################
# Project UNDYNE - MODULE 3
# #####################################################################################################################

# Drivers for the MCP3221 1 channel ADC utilising SMBUS rather than PIGPIO's i2c features.
# On old hardware version, use this for battery monitoring

import smbus
import time
import pigpio

i2c = smbus.SMBus(1)
pi = pigpio.pi()

address = 0x4D
class mcp3221():
    def readadc(self):
        V = i2c.read_i2c_block_data(address, 0x00, 2)
        V = self.voltage(V[0], V[1])
        return self.vbatt(V), self.vbatt(V)/4

    def voltage (self, msb, lsb):
        msb = msb << 8
        lsb = lsb
        v = msb + lsb

        return v*(3.3/4095)

    def vbatt(self, voltage):
        return voltage*5

# Print the estimated battery voltage... Not accurate: Cell's don't experience equal discharge rates...
# If my hardward worked, then it is possible to read the individual cell voltages of VBATT and determine
# if any fall under 3 volts per cell (on a seperate ADC)
