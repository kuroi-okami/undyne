# #####################################################################################################################
# Project UNDYNE - MODULE 1
# #####################################################################################################################
# PWM orientated motor drivers utilising python's smbus
# PCA9685 provides PWM signals to TLE8209-2SA H-Bridge motor drivers
# Hopefully it works :)
# It does ;)

import smbus
import pigpio
import time
i2c = smbus.SMBus(1) # RBPI 3B uses bus 1 for i2c communication
pi = pigpio.pi()

# ADC I2C addresses
ADDR_ADC_1 = 77
ADDR_ADC_4 = 76

# PWM  I2C address
ADDR_PWM = 64

# Register to set all registers
REG_ALL_CON = 0xFA

# First of PWM register (LED0_ON - LSB), 32 in total (LED0-8[ON/OFF time], LSB and MSB registers)
MOTOR_REG = 0x06
demandrange = 100

# Registers are mapped as such:

# LED0 - RIGHT THRUST (Forward)
# LED1 - RIGHT THRUST (Reverse)
# LED2 - RIGHT DIVE   (Forward)
# LED3 - RIGHT DIVE   (Reverse)
# LED4 - LEFT THRUST  (Forward)
# LED5 - LEFT THRUST  (Reverse)
# LED6 - LEFT DIVE    (Forward)
# LED7 - LEFT DIVE    (Reverse)

class motordriver():
    def initialise(self):
        # Enable output from the H-Bridge
        pi.write(27, pigpio.LOW)
        self.pwminit()

    def setdemand(self, demand):
        # Translate to 12-bit resolution
        for i in range(0, 4):
            #print("%s" % demand[i])
            if demand[i] > 100: demand[i] = 100
            elif demand[i] < -100: demand[i] = -100

            demand[i] = self.demandscale(demand[i], demandrange)
            #print("%s" % demand[i])

        block = [0] * 32
        demand, block = self.mapdemand(demand, block)
        #block = [0, 0, 255, 15, 0, 0, 0, 0, 0, 0, 255, 15, 0, 0, 0, 0, 0, 0, 255, 15, 0, 0, 0, 0, 0, 0, 255, 15, 0, 0, 0, 0]
        i2c.write_i2c_block_data(ADDR_PWM, MOTOR_REG, block)
        data = i2c.read_i2c_block_data(ADDR_PWM, MOTOR_REG, 32)




    def deactivate(self):
        offblock = [0] * 32
        self.setall(offblock)
        data = i2c.read_i2c_block_data(ADDR_PWM, MOTOR_REG, 32)
        #print(data)
        #pi.write(27, pigpio.HIGH)

    def pwminit(self):
        # Mode settings
        mode1 = [0xA0, 0x04]
        sleep = [0xB0, 0x04]
        #print (mode1, sleep)
        # Commence the sleep period - Required to set prescaler bit (effects frequency)
        i2c.write_i2c_block_data(ADDR_PWM, 0x00, sleep)
        data = i2c.read_i2c_block_data(ADDR_PWM, 0x00, 2)
        #print(data)
        # Write PWM frequency
        freq = [0x03]
        i2c.write_i2c_block_data(ADDR_PWM, 0xFE, freq)
        freq = i2c.read_i2c_block_data(ADDR_PWM, 0xFE, 1)
        #print(freq)
        # Write to mode registers 1 and 2
        i2c.write_i2c_block_data(ADDR_PWM, 0x00, mode1)
        # Read back the mode registers
        mode = i2c.read_i2c_block_data(ADDR_PWM, 0x00, 2)
        #print(mode)

    def setall(self, allblock):
        i2c.write_i2c_block_data(ADDR_PWM, REG_ALL_CON, allblock)

    def mapdemand(self, demand, datablock):
        # LT, LD, RT, RD motor registers
        registers = [30, 20, 14, 4]
        # encode the demand accross 32 bytes
        for i in range(0,4):
            #Thrust Phase
            if (i%2 == 0):
                # Forward PWM - Thrust
                if (demand[i] >= 0):
                    datablock[registers[i]] = demand[i]
                    datablock[registers[i]+1] = demand[i] >> 8
                # Reverse PWM - Thrust
                else:
                    datablock[registers[i] - 4] = abs(demand[i])
                    datablock[registers[i] - 3] = int(abs(demand[i])) >> 8
            else:
                # Ensure max demand isn't 4095
                if (demand[i] == 4095):
                    demand[i] = 4094
                elif (demand[i] == -4095):
                    demand[i] = -4094

                # Forward PWM - Dive
                if (demand[i] >= 0):
                    datablock[registers[i]] = 4095 - (demand[i])
                    datablock[registers[i] + 1] = int(4095 - abs(demand[i])) >> 8
                # Reverse PWM - Dive
                else:
                    datablock[registers[i] - 4] = 4095 -(abs(demand[i]))
                    datablock[registers[i] - 3] = int(4095 - (abs(demand[i]))) >> 8

        return demand, datablock

    def demandscale(self, demand, demandrange):
        demandscalar = 4095/demandrange
        return int(demand * demandscalar)


    #def setdemand(self, demand):
    #    print("Set motor demand (+-", demandrange, ")")
    #    demand[0] = input("Left Thrust: ")
    #    demand[1] = input("Right Thrust: ")
    #    demand[2] = input("Dive/Surface: ")
    #    demand[3] = demand[2]
    #    return demand

# #####################################################################################








