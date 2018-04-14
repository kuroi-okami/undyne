# #####################################################################################################################
# Project UNDYNE - MODULE 5 (Class)
# #####################################################################################################################

# Drivers fo the BNO055 IMU utilising 'import serial'
import serial
import time
from math import sqrt

# May it work, friend...
# Page id register definition
BNO055_PAGE_ID_ADDR                  = 0X07

# PAGE0 REGISTER DEFINITION START
BNO055_CHIP_ID_ADDR                  = 0x00
BNO055_ACCEL_REV_ID_ADDR             = 0x01
BNO055_MAG_REV_ID_ADDR               = 0x02
BNO055_GYRO_REV_ID_ADDR              = 0x03
BNO055_SW_REV_ID_LSB_ADDR            = 0x04
BNO055_SW_REV_ID_MSB_ADDR            = 0x05
BNO055_BL_REV_ID_ADDR                = 0X06

# Accel data register
BNO055_ACCEL_DATA_X_LSB_ADDR         = 0X08
BNO055_ACCEL_DATA_X_MSB_ADDR         = 0X09
BNO055_ACCEL_DATA_Y_LSB_ADDR         = 0X0A
BNO055_ACCEL_DATA_Y_MSB_ADDR         = 0X0B
BNO055_ACCEL_DATA_Z_LSB_ADDR         = 0X0C
BNO055_ACCEL_DATA_Z_MSB_ADDR         = 0X0D

# Mag data register
BNO055_MAG_DATA_X_LSB_ADDR           = 0X0E
BNO055_MAG_DATA_X_MSB_ADDR           = 0X0F
BNO055_MAG_DATA_Y_LSB_ADDR           = 0X10
BNO055_MAG_DATA_Y_MSB_ADDR           = 0X11
BNO055_MAG_DATA_Z_LSB_ADDR           = 0X12
BNO055_MAG_DATA_Z_MSB_ADDR           = 0X13

# Gyro data registers
BNO055_GYRO_DATA_X_LSB_ADDR          = 0X14
BNO055_GYRO_DATA_X_MSB_ADDR          = 0X15
BNO055_GYRO_DATA_Y_LSB_ADDR          = 0X16
BNO055_GYRO_DATA_Y_MSB_ADDR          = 0X17
BNO055_GYRO_DATA_Z_LSB_ADDR          = 0X18
BNO055_GYRO_DATA_Z_MSB_ADDR          = 0X19

# Euler data registers
BNO055_EULER_H_LSB_ADDR              = 0X1A
BNO055_EULER_H_MSB_ADDR              = 0X1B
BNO055_EULER_R_LSB_ADDR              = 0X1C
BNO055_EULER_R_MSB_ADDR              = 0X1D
BNO055_EULER_P_LSB_ADDR              = 0X1E
BNO055_EULER_P_MSB_ADDR              = 0X1F

# Quaternion data registers
BNO055_QUATERNION_DATA_W_LSB_ADDR    = 0X20
BNO055_QUATERNION_DATA_W_MSB_ADDR    = 0X21
BNO055_QUATERNION_DATA_X_LSB_ADDR    = 0X22
BNO055_QUATERNION_DATA_X_MSB_ADDR    = 0X23
BNO055_QUATERNION_DATA_Y_LSB_ADDR    = 0X24
BNO055_QUATERNION_DATA_Y_MSB_ADDR    = 0X25
BNO055_QUATERNION_DATA_Z_LSB_ADDR    = 0X26
BNO055_QUATERNION_DATA_Z_MSB_ADDR    = 0X27

# Linear acceleration data registers
BNO055_LINEAR_ACCEL_DATA_X_LSB_ADDR  = 0X28
BNO055_LINEAR_ACCEL_DATA_X_MSB_ADDR  = 0X29
BNO055_LINEAR_ACCEL_DATA_Y_LSB_ADDR  = 0X2A
BNO055_LINEAR_ACCEL_DATA_Y_MSB_ADDR  = 0X2B
BNO055_LINEAR_ACCEL_DATA_Z_LSB_ADDR  = 0X2C
BNO055_LINEAR_ACCEL_DATA_Z_MSB_ADDR  = 0X2D

# Gravity data registers
BNO055_GRAVITY_DATA_X_LSB_ADDR       = 0X2E
BNO055_GRAVITY_DATA_X_MSB_ADDR       = 0X2F
BNO055_GRAVITY_DATA_Y_LSB_ADDR       = 0X30
BNO055_GRAVITY_DATA_Y_MSB_ADDR       = 0X31
BNO055_GRAVITY_DATA_Z_LSB_ADDR       = 0X32
BNO055_GRAVITY_DATA_Z_MSB_ADDR       = 0X33

# Temperature data register
BNO055_TEMP_ADDR                     = 0X34

# Status registers
BNO055_CALIB_STAT_ADDR               = 0X35
BNO055_SELFTEST_RESULT_ADDR          = 0X36
BNO055_INTR_STAT_ADDR                = 0X37

BNO055_SYS_CLK_STAT_ADDR             = 0X38
BNO055_SYS_STAT_ADDR                 = 0X39
BNO055_SYS_ERR_ADDR                  = 0X3A

# Unit selection register
BNO055_UNIT_SEL_ADDR                 = 0X3B
BNO055_DATA_SELECT_ADDR              = 0X3C

# Mode registers
BNO055_OPR_MODE_ADDR                 = 0X3D
BNO055_PWR_MODE_ADDR                 = 0X3E

BNO055_SYS_TRIGGER_ADDR              = 0X3F
BNO055_TEMP_SOURCE_ADDR              = 0X40

# Axis remap registers
BNO055_AXIS_MAP_CONFIG_ADDR          = 0X41
BNO055_AXIS_MAP_SIGN_ADDR            = 0X42

# Axis remap values
AXIS_REMAP_X                         = 0x00
AXIS_REMAP_Y                         = 0x01
AXIS_REMAP_Z                         = 0x02
AXIS_REMAP_POSITIVE                  = 0x00
AXIS_REMAP_NEGATIVE                  = 0x01

# SIC registers
BNO055_SIC_MATRIX_0_LSB_ADDR         = 0X43
BNO055_SIC_MATRIX_0_MSB_ADDR         = 0X44
BNO055_SIC_MATRIX_1_LSB_ADDR         = 0X45
BNO055_SIC_MATRIX_1_MSB_ADDR         = 0X46
BNO055_SIC_MATRIX_2_LSB_ADDR         = 0X47
BNO055_SIC_MATRIX_2_MSB_ADDR         = 0X48
BNO055_SIC_MATRIX_3_LSB_ADDR         = 0X49
BNO055_SIC_MATRIX_3_MSB_ADDR         = 0X4A
BNO055_SIC_MATRIX_4_LSB_ADDR         = 0X4B
BNO055_SIC_MATRIX_4_MSB_ADDR         = 0X4C
BNO055_SIC_MATRIX_5_LSB_ADDR         = 0X4D
BNO055_SIC_MATRIX_5_MSB_ADDR         = 0X4E
BNO055_SIC_MATRIX_6_LSB_ADDR         = 0X4F
BNO055_SIC_MATRIX_6_MSB_ADDR         = 0X50
BNO055_SIC_MATRIX_7_LSB_ADDR         = 0X51
BNO055_SIC_MATRIX_7_MSB_ADDR         = 0X52
BNO055_SIC_MATRIX_8_LSB_ADDR         = 0X53
BNO055_SIC_MATRIX_8_MSB_ADDR         = 0X54

# Accelerometer Offset registers
ACCEL_OFFSET_X_LSB_ADDR              = 0X55
ACCEL_OFFSET_X_MSB_ADDR              = 0X56
ACCEL_OFFSET_Y_LSB_ADDR              = 0X57
ACCEL_OFFSET_Y_MSB_ADDR              = 0X58
ACCEL_OFFSET_Z_LSB_ADDR              = 0X59
ACCEL_OFFSET_Z_MSB_ADDR              = 0X5A

# Magnetometer Offset registers
MAG_OFFSET_X_LSB_ADDR                = 0X5B
MAG_OFFSET_X_MSB_ADDR                = 0X5C
MAG_OFFSET_Y_LSB_ADDR                = 0X5D
MAG_OFFSET_Y_MSB_ADDR                = 0X5E
MAG_OFFSET_Z_LSB_ADDR                = 0X5F
MAG_OFFSET_Z_MSB_ADDR                = 0X60

# Gyroscope Offset register s
GYRO_OFFSET_X_LSB_ADDR               = 0X61
GYRO_OFFSET_X_MSB_ADDR               = 0X62
GYRO_OFFSET_Y_LSB_ADDR               = 0X63
GYRO_OFFSET_Y_MSB_ADDR               = 0X64
GYRO_OFFSET_Z_LSB_ADDR               = 0X65
GYRO_OFFSET_Z_MSB_ADDR               = 0X66

# Radius registers
ACCEL_RADIUS_LSB_ADDR                = 0X67
ACCEL_RADIUS_MSB_ADDR                = 0X68
MAG_RADIUS_LSB_ADDR                  = 0X69
MAG_RADIUS_MSB_ADDR                  = 0X6A

# Power modes
POWER_MODE_NORMAL                    = 0X00
POWER_MODE_LOWPOWER                  = 0X01
POWER_MODE_SUSPEND                   = 0X02

# Operation mode settings
OPERATION_MODE_CONFIG                = 0X00
OPERATION_MODE_ACCONLY               = 0X01
OPERATION_MODE_MAGONLY               = 0X02
OPERATION_MODE_GYRONLY               = 0X03
OPERATION_MODE_ACCMAG                = 0X04
OPERATION_MODE_ACCGYRO               = 0X05
OPERATION_MODE_MAGGYRO               = 0X06
OPERATION_MODE_AMG                   = 0X07
OPERATION_MODE_IMUPLUS               = 0X08
OPERATION_MODE_COMPASS               = 0X09
OPERATION_MODE_M4G                   = 0X0A
OPERATION_MODE_NDOF_FMC_OFF          = 0X0B
OPERATION_MODE_NDOF                  = 0X0C

class bno055():
    def __init__(self):
        #Baud rate of 115200 is required... Otherwise errors ye shall have
        self.serial = serial.Serial("/dev/ttyAMA0", 115200, timeout=2)

    def writecommand(self, command, ack= True, maxattempts=3):
        attempt = 0
        while True:
            self.serial.flushInput()
            self.serial.write(command)
            if ack == False:
                return
            response = bytearray(self.serial.read(2))
            if not (response[0] == 0xEE and response[1] == 0x07):
                return response
            attempt += 1

            if attempt == maxattempts:
                raise RuntimeError("Too many re-send attempts")

    def serialwrite(self, address, data, ack = True):
        command = bytearray(4 + len(data))
        command[0] = 0xAA
        command[1] = 0x00
        command[2] = address & 0xFF
        command[3] = len(data) & 0xFF
        command[4:] = map(lambda x: x & 0xFF, data)

        response = self.writecommand(command, ack=ack)
        if response[0] != 0xEE and response[1] != 0x01:
            raise RuntimeError("Write unsuccessful")

    def serialwritebyte(self, address, data, ack = True):
        command = bytearray(5)
        command[0] = 0xAA
        command[1] = 0x00
        command[2] = address & 0xFF
        command[3] = 1
        command[4] = data & 0xFF
        response = self.writecommand(command, ack=ack)
        if ack and response[0] != 0xEE and response[1] != 0x01:
            raise RuntimeError("Write unsuccessful")

    def signedreadbyte(self, address):
        data = self.serialread(address, 1)[0]
        if data > 127:
            return data - 256
        else:
            return data

    def serialread(self, address, count):
        command = bytearray(4)
        command[0] = 0xAA
        command[1] = 0x01
        command[2] = address & 0xFF
        command[3] = count & 0xFF
        response = self.writecommand(command)
        if not response[0] == 0xBB:
            raise RuntimeError("Read unsuccessful")
        count = response[1]
        response = bytearray(self.serial.read(count))
        if response is None or len(response) != count:
            raise RuntimeError("We have issues, my friend...")
        return response

    def modeset(self, mode):
        self.serialwritebyte(BNO055_OPR_MODE_ADDR, mode & 0xFF)
        time.sleep(0.03)

    def initalise(self, mode = OPERATION_MODE_NDOF):
        try:
            self.serialwritebyte(BNO055_PAGE_ID_ADDR, 0, ack=False)
        except IOError:
            pass

        self.modeset(OPERATION_MODE_CONFIG)
        self.serialwritebyte(BNO055_PAGE_ID_ADDR, 0)
        bnoID = self.serialread(BNO055_CHIP_ID_ADDR, 1)
        self.serialwritebyte(BNO055_SYS_TRIGGER_ADDR, 0x20, ack=False)
        time.sleep(0.65)
        self.serialwritebyte(BNO055_PWR_MODE_ADDR, 0x00)
        self.modeset(mode)

    def readvector(self, address, count = 3):
        # Method to read vector quantities and return them as a tuple
        data = self.serialread(address, count*2)
        result = [0]*count
        for i in range(count):
            result[i] = (data[(2*i) + 1] << 8) + (data[2*i] & 0xFFFF)
            if result[i] > 32767:
                result[i] -= 65536
        return result

    def geteuler(self):
        # Return absolute orientation as a tuple of heading, roll, pitch measured in degrees
        heading, roll, pitch = self.readvector(BNO055_EULER_H_LSB_ADDR)
        return (heading/16.0, roll/16.0, pitch/16.0)

    def getmagnetometer(self):
        # Return the magnetometer reading as a tuple of values measured in micro-Tesla
        x, y, z = self.readvector(BNO055_MAG_DATA_X_LSB_ADDR)
        return (x/16.0, y/16.0, z/16.0)

    def getgyroscope(self):
        # Return the angular velocity reading as a tuple measured in degrees per second
        x, y ,z = self.readvector(BNO055_GYRO_DATA_X_LSB_ADDR)
        return (x/900.0, y/900.0, z/900.0)

    def getaccelerometer(self):
        # Return accleralerometer reading as a tuple measured in meters per second squared
        x, y, z = self.readvector(BNO055_ACCEL_DATA_X_LSB_ADDR)
        return (x/100.0, y/100.0, z/100.0)

    def getlinearaccleration(self):
        # Return linear accleration reading (purely from movement) reading as a tuple measured
        # in meters per second squared
        x, y, z = self.readvector(BNO055_LINEAR_ACCEL_DATA_X_LSB_ADDR)
        return(x/100.0, y/100.0, z/100.0)

    def getgravity(self):
        # Return gravitational accleration reading as a tuple measured in meters per second sqaured
        x, y, z = self.readvector(BNO055_GRAVITY_DATA_X_LSB_ADDR)
        x, y, z = x/100.0, y/100.0, z/100.0
        resultant = sqrt(x*x + y*y + z*z)
        return (resultant, x, y, z)


    def getquaternion(self):
        # Return current orientation as a tuple of quaternion values
        w, x, y, z = self.readvector(BNO055_QUATERNION_DATA_W_LSB_ADDR, count=4)
        scale = (1.0 / (1<<14))
        return (x*scale, y*scale, z*scale, w*scale)

    def gettemperature(self):
        # Return the current temperature in celsius
        return self.signedreadbyte(BNO055_TEMP_ADDR)

    def filteraccleration(self):
        alpha = 1/8
        x, y, z =self.getlinearaccleration()
        time.sleep(0.05)
        xn, yn, zn = self.getlinearaccleration()
        xn = x * alpha + (xn * (1 - alpha))
        yn = y * alpha + (yn * (1 - alpha))
        zn = z * alpha + (zn * (1 - alpha))
        return xn, yn, zn

    def getvelocity(self):
        stime = time.time()
        xt, yt, zt = 0, 0, 0
        for i in range(5):
            x, y, z = self.filteraccleration()
            xt += x
            #yt += y
            #zt += z
        stime = (time.time() - stime)/ 5
        x = xt*stime
        #y = yt*stime
        #z = zt*stime
        resultant = x
        return resultant #- 0.065 Slight hack... Device seems to possess a velocity of ~0.065 while stationary

    def getposition(self, previoustime, previousvelocity= 0, previousposition= 0): # Returns position and velocity with respect to the X axis
        velocity = self.getvelocity()
        currenttime = time.time()
        deltatime = currenttime - previoustime
        #print(deltatime)
        position = (((velocity + previousvelocity) * deltatime) / 2) + previousposition
        return position, velocity, currenttime






