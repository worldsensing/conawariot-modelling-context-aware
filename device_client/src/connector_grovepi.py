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
        return randrange(255)
    else:
        import grovepi
        return grovepi.analogRead(pin) // 4  # 1024 to 256 precision


def send_digital_value(pin, value):
    print(f"send_digital_value: pin {pin}, value {value}")
    if PC_MODE:
        pass
    else:
        import grovepi
        grovepi.digitalWrite(pin, value)
