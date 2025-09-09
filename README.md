# ESP32-C3 Temperature Switch for Home Assistant


A MicroPython-based "project" for ESP32-C3 that reads temperature from a DHT11 sensor and controls any binary entity in Home Assistant when temperature thresholds are reached.


## Overview


The script's logic is such that when the temperature reaches 26 degrees Celsius, the switch is turned on, and when it drops to 24 degrees Celsius, it is turned off.

You can declare your own variables in config.py, but the temperature thresholds remain in main.py. (I'll move them in the future.)

The sensor is updated every second, so if you do not plan to use external power, change this value.

## Tested on

- Espressif ESP32-C3
