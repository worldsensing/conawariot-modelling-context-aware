# python_client

This client has been developed for Raspberry Pi devices. Also, it has compatibility with computers,
emulating the information as if the computer is a Raspberry Pi.

## Setup

- Follow the steps in: https://github.com/DexterInd/GrovePi/tree/master/Script
- Run `pip install -r requirements.txt`

### Configuration

All the configuration to be done is located at `__init__.py`.

#### PC or Raspberry Pi

The code presented in this project can be executed either on a normal computer or in a Raspberry Pi
with GrovePi on top of it. If you are in the first case, set `PC_MODE` to `True`, otherwise, set it
to `False` to enable GrovePi code. When disabled the commands to be sent to the GrovePi are
converted into log messages.

#### Sensors

##### Tilt Sensor - Grove (6-Axis Accelerometer&Gyroscope)

The Light sensor by [Grove](https://www.seeedstudio.com/Grove-6-Axis-Accelerometer-Gyroscope.
html) is the one used in the project. When configuring a Raspberry to act as a Sensor, set it 
like this:

`SENSOR_CONFIGURED = "TILT"`.

#### Actuators

No actuators have been instantiated. Although the system supports them.

#### Others

LED lights are configured in the project, mainly for use as information to check if the workflow is
OK.

- Green LED: https://www.seeedstudio.com/Grove-Green-LED.html
- Red LED: https://www.seeedstudio.com/Grove-Red-LED.html

### Troubleshooting

- `ImportError: No module named 'di_i2c'`

```bash
$ sudo apt --fix-broken install
$ sudo apt-get install libffi-dev
$ cd /home/pi/Dexter/lib/Dexter/RFR_Tools/miscellaneous/
$ sudo python3 setup.py install
```

Source: https://forum.dexterindustries.com/t/trouble-installing-grovepi/6119/12