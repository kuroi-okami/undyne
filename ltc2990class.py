# #####################################################################################################################
# Project UNDYNE - MODULE 2
# #####################################################################################################################

# Drivers for the LTC2990 4 channel ADC utilising SMBUS rather than PIGPIO's i2c features.
# IT WORKS
# FUCK YEAH
# FUCK PIGPIO

import smbus
import time
i2c = smbus.SMBus(1) # RBPI 3B uses bus 1 for i2c communication

address = 0x4C
singlemode = 0x5F # 5F provides single aquisition of T, V1, V2, V3, V4 when written to control register
repeatmode = 0x3F # 3F provides repeated aquisition of T, V1, V2, V3, V4 when written

sreg = 0x00 # Status
creg = 0x01 # Control
treg = 0x02 # Trigger
tmpreg = [0x04, 0x05] # Temperature
voltreg = [0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D] # V1, V2, V3, V4 (MSB and LSB)
vccreg = [0x0E, 0x0F]

#control = i2c.read_byte_data(address, creg) # Reads the initial control register
class ltc2990():
    # Initializing...
    def initadc(self):
        i2c.write_byte_data(address, creg, singlemode) # Write desired mode to the control register
        i2c.write_byte_data(address, treg, 0x00) # Trigger conversion
        time.sleep(1) # Give it a minute (well, a second) to think

        status = i2c.read_byte_data(address, sreg)
        control = i2c.read_byte_data(address, creg)
        #print("%s %s" %(status, control))

    def t1(self):
        TEMPmsb = i2c.read_byte_data(address, tmpreg[0])
        TEMPlsb = i2c.read_byte_data(address, tmpreg[1])
        return self.temp(TEMPmsb, TEMPlsb)


    def v1(self):
        V1msb = i2c.read_byte_data(address, voltreg[0])
        V1lsb = i2c.read_byte_data(address, voltreg[1])
        return self.voltage(V1msb, V1lsb)


    def v2(self):
        V2msb = i2c.read_byte_data(address, voltreg[2])
        V2lsb = i2c.read_byte_data(address, voltreg[3])
        return self.voltage(V2msb, V2lsb)

    def v3(self):
        V3msb = i2c.read_byte_data(address, voltreg[4])
        V3lsb = i2c.read_byte_data(address, voltreg[5])
        return self.voltage(V3msb, V3lsb)

    def v4(self):
        V4msb = i2c.read_byte_data(address, voltreg[6])
        V4lsb = i2c.read_byte_data(address, voltreg[7])
        return self.voltage(V4msb, V4lsb)

    def vcc(self):
        VCCmsb = i2c.read_byte_data(address, vccreg[0])
        VCClsb = i2c.read_byte_data(address, vccreg[1])
        return self.voltage(VCCmsb, VCClsb) + 2.5

    def temp(self, msb, lsb):
        # Determine flags which are set/unset
        DV = msb & 0b10000000 # Data Valid   - If greater than zero, data is new
        SS = msb & 0b01000000 # Sensor Short - If V1 voltage is too low during temp reading, will be greater than zero
        SO = msb & 0b00100000 # Sensor Open  - If V1 voltage is too high during temp reading, will be greater than zero

        msb = format(msb, '08b')[3:]
        lsb = format(lsb, '08b')
        temp = int(msb + lsb, 2)/16

        return temp #, DV, SS, SO

    def voltage(self, msb,lsb):
        # Determine flags which are set/unset
        DV = msb & 0b10000000   # Data Valid - If greater than zero, data is new
        SIGN = msb & 0b01000000 # Sign Bit - If greater than zero, implies negative voltage

        msb = format(msb, '08b')[2:]
        lsb = format(lsb, '08b')
        if (SIGN == 0):
            volt = int(msb + lsb, 2) * 0.00030518
        else:
            volt = int(msb + lsb, 2) * -0.00030518

        return volt

    def readadc(self):
        self.initadc()
        T = self.t1()
        V1 = self.v1()
        V2 = self.v2()
        V3 = self.v3()
        V4 = self.v4()
        VCC = self.vcc()

        print("Temperature    : %0.2f Celsius" % T)
        print("Voltage 1      : %0.2f Volts" % V1)
        print("Voltage 2      : %0.2f Volts" % V2)
        print("Voltage 3      : %0.2f Volts" % V3)
        print("Voltage 4      : %0.2f Volts" % V4)
        print("Voltage CC     : %0.2f Volts" % VCC)

    def pressure(self):
        self.initadc()
        T = self.t1()
        V1 = self.v1()
        print("Temperature: %s Celsius" % T)
        print("Voltage 1  : %s Volts" % V1)

        return V1, T

    def ingress(self):
        self.initadc()
        V2 = self.v2()
        print("Voltage 2  : %s Volts" % V2)

        return V2



















