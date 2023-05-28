#! /usr/bin/python2

import time
import sys
import pyfiglet
import RPi.GPIO as GPIO
from hx711 import HX711

def config_doghouse_weight(dtpin = 27, sckpin=17):
    print("Starting to config the doghouse_weight") 
    referenceUnit = 1
    hx = HX711(dtpin, sckpin)
    hx.set_reading_format("MSB", "MSB")
    #hx.set_reference_unit(113)
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()
    print("Done to config the doghouse_weight") 

    return hx

def cleanAndExit():
        print("Cleaning...")
        GPIO.cleanup()
        print("Bye!")
        sys.exit()

def get_doghouse_weight(hx, dtpin = 5, sckpin=27, sleeptime = 0.5):

    while True:
        try:
         dog_weight = max((hx.get_weight(27)/(-25), 0))
         print(f"Dog's weight is:{int(dog_weight)}")

         hx.power_down()
         hx.power_up()
         time.sleep(1)
         return dog_weight   
        
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
        '''
        else:
            print("Cannot get data, try again")
            continue 
        '''
        
if __name__ == "__main__":  
    hx = config_doghouse_weight()   
    while True :
        get_doghouse_weight(hx=hx)