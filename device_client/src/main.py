import time
from threading import Thread

import schedule
from flask import Flask

from __init__ import FLASK_ENABLED, SENSOR_CONFIGURED
from api import api
from connector_grovepi import pin_mode, send_digital_value
from grove import read_sensor_tilt

if FLASK_ENABLED:
    app = Flask(__name__)
    app.register_blueprint(api)

if SENSOR_CONFIGURED == "TILT_B_INCL":
    TILT_SENSOR = 1  # Analog port 1
    RED_LED = 2  # Digital port 2
    RED_LED_THRESHOLD = 100

    pin_mode(RED_LED, "OUTPUT")
    send_digital_value(RED_LED, 0)


def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    print("Starting up code...")

    print("Sensor configured is: " + SENSOR_CONFIGURED)
    if SENSOR_CONFIGURED == "TILT_B_INCL":
        read_sensor_tilt()

        schedule.every(1).seconds.do(read_sensor_tilt)

    print("Setup Scheduler...")
    t = Thread(target=run_schedule)
    t.start()

    if FLASK_ENABLED:
        print("Setup Flask server...")
        app.run(host="0.0.0.0", port=8001, use_reloader=False)