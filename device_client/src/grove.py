from connector_grovepi import send_digital_value, read_analog_value

from src.core import post_sensor_observation


def read_sensor_information():
    from main import TILT_SENSOR, RED_LED

    try:
        send_digital_value(RED_LED, 1)
        resistance_value = read_analog_value(TILT_SENSOR)
        print(f"Value is: {resistance_value}")
        observation_id = post_sensor_observation(resistance_value)
    except IOError as error:
        print("Error")
        print(error)
    finally:
        send_digital_value(RED_LED, 0)
