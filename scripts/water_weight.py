#! /usr/bin/python3

import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711


def config_water_weight(dtpin=5, sckpin=6, referenceUnit=-470):
    try:
        print("Starting to config the water weight")
        hx = HX711(dtpin, sckpin)
        hx.set_reading_format("MSB", "MSB")
        hx.set_reference_unit(referenceUnit)
        hx.reset()
        hx.tare()
        print("Finishing to config the water weight")
        return hx

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()


def get_water_weight(hx, sleeptime=0.5):
    print("Checking water's weight...")
    water_weight = None
    while not water_weight:
        try:
            water_weight = max(0, int(hx.get_weight()))
            print(f"Water's weight is: {water_weight} ml")
            hx.power_down()
            hx.power_up()
            time.sleep(sleeptime)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()

    return water_weight


if __name__ == "__main__":
    hx = config_water_weight()
    while True:
        get_water_weight(hx=hx)
