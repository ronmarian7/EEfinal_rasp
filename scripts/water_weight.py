#! /usr/bin/python2

import time
import sys
import pyfiglet
import RPi.GPIO as GPIO
from hx711 import HX711

def config(dtpin = 5, sckpin=6):
   
    referenceUnit = 1
    hx = HX711(dtpin, sckpin)
    hx.set_reading_format("MSB", "MSB")
    #hx.set_reference_unit(113)
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()
    return hx

def cleanAndExit():
        print("Cleaning...")
        GPIO.cleanup()
        print("Bye!")
        sys.exit()

def get_water_weight(hx, dtpin = 5, sleeptime = 0.5):
    print("Checking water's weight...")

    while True:
        try:
            water_weight = max(0, int((hx.get_weight(dtpin))/(-470))) 
            print(f"Water's weight is: {(water_weight)} ml.")
            hx.power_down()
            hx.power_up()
            time.sleep(sleeptime)
            return water_weight
        
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
        '''
        else:
            print("Cannot get data, try again")
            continue 
        '''
        
if __name__ == "__main__":  
    while(1):
        hx = config()   
        get_water_weight(hx=hx)