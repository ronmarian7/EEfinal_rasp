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


def get_water_weight(hx, sleeptime=0.5, const_vas=0):
    # print("Checking water's weight...")
    water_weight = None
    while water_weight == None:
        try:
            water_weight = max(0, int(hx.get_weight()) - const_vas) 
            print(f"Water's weight is: {water_weight} ml")
            hx.power_down()
            hx.power_up()
            time.sleep(sleeptime)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()

    return water_weight


if __name__ == "__main__":
    from PinConfig import *
    hx = config_water_weight(dtpin=WATER_WEIGHT_DTPIN, sckpin=WATER_WEIGHT_SCKPIN,
                                         referenceUnit=WATER_WEIGHT_REFERENCE_UNIT)
    while True:
        get_water_weight(hx=hx)
        time.sleep(1)
