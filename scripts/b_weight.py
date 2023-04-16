#! /usr/bin/python2

import time
import sys

EMULATE_HX711=False

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Scaling stoped")
    sys.exit()

hx1 = HX711(5, 6)
hx1.set_reading_format("MSB", "MSB")

hx1.set_reference_unit(referenceUnit)

hx1.reset()

hx1.tare()

print("Checking food's weight...")


while True:
    try:
       
        val = max(0, int(hx1.get_weight(23)))
        print(f"Food's weight is:{val}")

        hx1.power_down()
        hx1.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
