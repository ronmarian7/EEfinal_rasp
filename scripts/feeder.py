import RPi.GPIO as GPIO
import time

# GPIO.setmode(GPIO.BCM)

# receives two variables, portion (default 1), and pin (default 13) - represents the GPIO pin number
def feed(portion = 1, pin = 13, sleeptime = 4):
    GPIO.setup(pin, GPIO.OUT)
    for i in range(portion):
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.5) # Wait for 0.5 seconds
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(sleeptime) # Wait for 4 seconds

if __name__ == '__main__':
    feed(4)  