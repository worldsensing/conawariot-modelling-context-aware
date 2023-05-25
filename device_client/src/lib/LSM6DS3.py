import sys
import time

import RPi.GPIO as GPIO
import smbus

# Sensor I2C Address
LSM6DS3_ADDR = 0x6a

# Register-specific values to read
ACCEL_LOW_X = 0x28
ACCEL_HIGH_X = 0x29
ACCEL_LOW_Y = 0x2A
ACCEL_HIGH_Y = 0x2B
ACCEL_LOW_Z = 0x2C
ACCEL_HIGH_Z = 0x2D

GYRO_LOW_X = 0x22
GYRO_HIGH_X = 0x23
GYRO_LOW_Y = 0x24
GYRO_HIGH_Y = 0x25
GYRO_LOW_Z = 0x26
GYRO_HIGH_Z = 0x27

# Register-specific values to write
CTRL1_XL = 0x10  # Accelerometer configuration
CTRL2_G = 0x11  # Gyroscope configuration

# use the bus that matches your raspi version
rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)


def decimal_to_binary(int_value):
    return "{0:08b}".format(int_value)


def two_complement_two_bytes(val_str):
    val = int(val_str, 2)
    b = val.to_bytes(2, byteorder=sys.byteorder, signed=False)
    return int.from_bytes(b, byteorder=sys.byteorder, signed=True)


class LSM6DS3:
    # Write ´data´ to a ´reg´ on the I2C device
    def __write_reg(self, data, reg):
        bus.write_byte_data(LSM6DS3_ADDR, reg, data)
        time.sleep(0.01)

    # Read from the ´reg´ register
    def __read_reg(self, reg):
        value = bus.read_byte_data(LSM6DS3_ADDR, reg)
        time.sleep(0.01)
        return value

    def __init__(self):
        dataToWrite = 0
        dataToWrite |= 0b00010000  # ODR_XL Low power mode
        dataToWrite |= 0b00000000  # FX_XL Full-scale selection in +-2g
        dataToWrite |= 0b00000011  # BW_XL Anti-aliasing filter in 50 Hz
        self.__write_reg(dataToWrite, CTRL1_XL)

        dataToWrite = 0
        dataToWrite |= 0b00010000  # ODR_G Low power mode
        dataToWrite |= 0b00001000  # FS_G Full-scale selection in 1000 dps
        dataToWrite |= 0b00000000  # FS_125 Full-scale selection not in 125 dps
        self.__write_reg(dataToWrite, CTRL2_G)

        time.sleep(0.05)

    def read_acceleration_x(self):
        return self.get_value_int_from_register_address(ACCEL_HIGH_X, ACCEL_LOW_X)

    def read_acceleration_y(self):
        return self.get_value_int_from_register_address(ACCEL_HIGH_Y, ACCEL_LOW_Y)

    def read_acceleration_z(self):
        return self.get_value_int_from_register_address(ACCEL_HIGH_Z, ACCEL_LOW_Z)

    def read_gyroscope_x(self):
        return self.get_value_int_from_register_address(GYRO_HIGH_X, GYRO_LOW_X)

    def read_gyroscope_y(self):
        return self.get_value_int_from_register_address(GYRO_HIGH_Y, GYRO_LOW_Y)

    def read_gyroscope_z(self):
        return self.get_value_int_from_register_address(GYRO_HIGH_Z, GYRO_LOW_Z)

    def get_value_int_from_register_address(self, high_register, low_register):
        high_value = self.__read_reg(high_register)
        low_value = self.__read_reg(low_register)
        output_high_bin = decimal_to_binary(high_value)
        output_low_bin = decimal_to_binary(low_value)
        output_int = two_complement_two_bytes(f"{output_high_bin}{output_low_bin}")
        return output_int
