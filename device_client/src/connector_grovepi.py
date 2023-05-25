from __init__ import PC_MODE


def pin_mode(pin, value):
    print(f"pin_mode: pin {pin}, value {value}")
    if PC_MODE:
        pass
    else:
        import grovepi
        grovepi.pinMode(pin, value)


def read_analog_value(pin):
    print(f"read_analog_value: pin {pin}")
    if PC_MODE:
        from random import randrange
        value = randrange(start=-9999, stop=9999)
    else:
        import grovepi
        value = grovepi.analogRead(pin) // 4  # 1024 to 256 precision

    return value


def read_3_axis_accelerometer_value():
    print(f"read_3_axis_accelerometer_value")
    if PC_MODE:
        from random import randrange
        acc_x = randrange(start=-32768, stop=32767)
        acc_y = randrange(start=-32768, stop=32767)
        acc_z = randrange(start=-32768, stop=32767)
    else:
        from lib.LSM6DS3 import LSM6DS3

        lsm6ds3 = LSM6DS3()

        try:
            acc_x = lsm6ds3.read_acceleration_x()
            acc_y = lsm6ds3.read_acceleration_y()
            acc_z = lsm6ds3.read_acceleration_z()
        except IOError as e:
            print("Unable to read from accelerometer, check the sensor and try again. Error is: ")
            print(e)

    return acc_x, acc_y, acc_z


def send_digital_value(pin, value):
    print(f"send_digital_value: pin {pin}, value {value}")
    if PC_MODE:
        pass
    else:
        import grovepi
        grovepi.digitalWrite(pin, value)