import time
from threading import Thread

import schedule
from flask import Flask

from __init__ import SENSOR_CONFIGURED
from api import api
from connector_grovepi import pin_mode, send_digital_value

app = Flask(__name__)
app.register_blueprint(api)

if SENSOR_CONFIGURED == "TILT":
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

    if SENSOR_CONFIGURED == "TILT":
        print("Setup Scheduler...")
        # read_sensor_information()

        # schedule.every(3).seconds.do(read_sensor_information)

        t = Thread(target=run_schedule)
        t.start()

    print("Setup Flask server...")
    app.run(host="0.0.0.0", port=8001, use_reloader=False)
