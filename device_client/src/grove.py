from connector_grovepi import send_digital_value, read_3_axis_accelerometer_value

from core import post_sensor_observation


def read_sensor_tilt():
    from main import RED_LED

    try:
        send_digital_value(RED_LED, 1)
        acc_x, acc_y, acc_z = read_3_axis_accelerometer_value()
        print(f"Value is: {acc_x}, {acc_y}, {acc_z}")

        post_sensor_observation(acc_x)
        # post_sensor_observation(acc_y)
        # post_sensor_observation(acc_z)
    except IOError as error:
        print("Error")
        print(error)
    finally:
        send_digital_value(RED_LED, 0)
