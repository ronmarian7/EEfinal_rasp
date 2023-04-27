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
hx2 = HX711(23, 24)
hx2.set_reading_format("MSB", "MSB")
#hx.set_reference_unit(92)
hx1.set_reference_unit(referenceUnit)
hx2.set_reference_unit(referenceUnit)

hx1.reset()
hx2.reset()

hx1.tare()
hx2.tare()

print("Checking food's weight...")


while True:
    try:
       
        val1 = max(0,(hx1.get_weight(5))/470)
        val2 = max(0,(hx1.get_weight(23))/470)
        print(f"Food1's weight is: {int((val1+val2))} gr.")
        

        hx1.power_down()
        hx1.power_up()
        hx2.power_down()
        hx2.power_up()
        time.sleep(0.01)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
