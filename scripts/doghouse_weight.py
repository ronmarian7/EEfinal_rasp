#! /usr/bin/python3

import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711


def config_doghouse_weight(dtpin=27, sckpin=17, referenceUnit=-25):
    try:
        print("Starting to config the doghouse_weight")
        hx = HX711(dtpin, sckpin)
        hx.set_reading_format("MSB", "MSB")
        hx.set_reference_unit(referenceUnit)
        hx.reset()
        hx.tare()
        print("Done to config the doghouse_weight")
        return hx

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()


def get_doghouse_weight(hx, sleeptime=0.5) -> int:
    dog_weight = None
    while dog_weight is None:
        try:
            dog_weight = max(0, int(hx.get_weight()))
            print(f"Dog's weight is:{dog_weight}")

            hx.power_down()
            hx.power_up()
            time.sleep(sleeptime)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()

    return dog_weight


if __name__ == "__main__":
    from PinConfig import *

    doghouse_weight_m = config_doghouse_weight(dtpin=DOGHOUSE_WEIGHT_DTPIN, sckpin=DOGHOUSE_WEIGHT_SCKPIN,
                                               referenceUnit=DOGHOUSE_REFERENCE_UNIT)
    while True:
        doghouse_weight = get_doghouse_weight(doghouse_weight_m)
        time.sleep(1)
