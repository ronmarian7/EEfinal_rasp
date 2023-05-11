#! /usr/bin/python2

import time
import sys
import pyfiglet

# Variables: dtpin(def=5), sckpin(def=6), sleeptime(def=0.5s), cautionthreshold(def=100ml)
def get_water_weight(dtpin = 5, sckpin=6, sleeptime = 0.5, cautionthreshold = 100):
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
            
        print("Bye!")
        sys.exit()

    hx = HX711(dtpin, sckpin)


    hx.set_reading_format("MSB", "MSB")


    #hx.set_reference_unit(113)
    hx.set_reference_unit(referenceUnit)

    hx.reset()

    hx.tare()

    print("Checking water's weight...")

    sampling_count=0
    while True:
        try:
        
            water_weight = max(0, int((hx.get_weight(dtpin))/(-470))) 
            sampling_count+=1
            print(f"Water's weight is: {(water_weight)} ml.")
            if(sampling_count>10):
                if (water_weight < cautionthreshold):
                    text = pyfiglet.figlet_format("CAUTION:\nWater needs a refill!", font="big")
                    print("\033[1;31m" + text + "\033[0m")
                    #print("\033[91m" + "CAUTION: Water needs a refill!" + "\033[0m")
            hx.power_down()
            hx.power_up()
            time.sleep(sleeptime)
            #return water_weight
        
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
        
        else:
            print("Cannot get data, try again")
            continue 
        
        
get_water_weight()