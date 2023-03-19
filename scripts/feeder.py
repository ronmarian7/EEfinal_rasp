import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)

def feed(portion = 1):
    for i in range(portion):
        GPIO.output(13, GPIO.LOW)
        time.sleep(0.5) # Wait for 0.5 seconds
        GPIO.output(13, GPIO.HIGH)
        time.sleep(4) # Wait for 4 seconds

feed(3)
