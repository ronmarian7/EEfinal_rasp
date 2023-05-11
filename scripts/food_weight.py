#! /usr/bin/python2

import time
import sys
import feeder
import time
import threading

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

# Variables: dtpin1(def=19), sckpin1(def=26), dtpin2(def=23), sckpin2(def=24) sleeptime(def=0.1s), feedingthreshold(def=100gr), portions(def=4), feedersleeptime(def=4s)
def handle_feeder(dtpin1 = 19, sckpin1 = 26, dtpin2 = 23, sckpin2 = 24, sleeptime = 0.1, feedingthreshold = 100, portions = 4, feedersleeptime = 4):

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
            
        print("Scaling stopped")
        sys.exit()

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
    sampling_count=0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    while True:
        try:
            food_weight1 = max(0,(hx1.get_weight(dtpin1))/470)
            food_weight2 = max(0,(hx2.get_weight(dtpin2))/470)
            sampling_count+=1
            total_food_weight=int(food_weight1+food_weight2)
            print(f"Food's weight is: {total_food_weight} gr.")
            if(sampling_count>5):
              if (total_food_weight)<feedingthreshold:
                 seconds = portions*feedersleeptime
                 print(f"Feeding dog, will take {seconds} seconds")
                 timer_thread = threading.Thread(target=countdown, args=(seconds,))
                 timer_thread.start()
                 feeder.feed(portions)
                 timer_thread.join()

            hx1.power_down()
            hx1.power_up()
            hx2.power_down()
            hx2.power_up()
            time.sleep(sleeptime)
            #return total_food_weight
        
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()

handle_feeder()
