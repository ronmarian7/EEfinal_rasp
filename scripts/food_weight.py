#! /usr/bin/python2

import time
import sys
import feeder
import time
import threading
import RPi.GPIO as GPIO
from hx711 import HX711

def countdown(seconds):
    for i in range(seconds, -1, -1):
        if i == 1:
            print("\r0{} second".format(i), end="")
        elif i < 10:
            print("\r0{} seconds".format(i), end="")
        else:
            print("\r{} seconds".format(i), end="")
                   
        time.sleep(1)

    print("\rDone Feeding!")


def cleanAndExit():
        print("Cleaning...")
        GPIO.cleanup()
      
        print("Scaling stopped")
        sys.exit()

def config(dtpin1 = 19, sckpin1 = 13, dtpin2 = 23, sckpin2 = 24):
    referenceUnit = 1 
    hx1 = HX711(dtpin1,sckpin1)
    hx1.set_reading_format("MSB", "MSB")
    hx2 = HX711(dtpin2, sckpin2)
    hx2.set_reading_format("MSB", "MSB")
    #hx.set_reference_unit(92)
    hx1.set_reference_unit(referenceUnit)
    hx2.set_reference_unit(referenceUnit)
    hx1.reset()
    hx2.reset()
    hx1.tare()
    hx2.tare() 
    return hx1,hx2

def handle_feeder(hx1,hx2, dtpin1 = 19, sckpin1 = 13, dtpin2 = 23, sckpin2 = 24, sleeptime = 0.1, feedingthreshold = 100,cur_ref_weight= 500, portions = 4, feedersleeptime = 4, feederpin = 26):

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
    while True:
        try:
            food_weight1 = max(0,(hx1.get_weight(dtpin1))/470)
            food_weight2 = max(0,(hx2.get_weight(dtpin2))/470)
            total_food_weight=int(food_weight1+food_weight2)
            print(f"Food's weight is: {total_food_weight} gr.")
            if total_food_weight<(cur_ref_weight-feedingthreshold):
                 seconds = portions*feedersleeptime
                 print(f"Feeding dog, will take {seconds} seconds")
                 timer_thread = threading.Thread(target=countdown, args=(seconds,))
                 timer_thread.start()
                 feeder.feed(portions,feederpin)
                 timer_thread.join()

            hx1.power_down()
            hx1.power_up()
            hx2.power_down()
            hx2.power_up()
            time.sleep(sleeptime)
            
            return total_food_weight
        
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


if __name__ == "__main__":  
    hx1,hx2 = config()   
    handle_feeder(hx1,hx2)
