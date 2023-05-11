import time
import board
import adafruit_dht
 
# Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT22(board.D4)
 
# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.

# Variable: pin(def=17), sleeptime(def=2.0)
def get_humidity_tmp(pin = 17, sleeptime = 2.0):

    dhtDevice = adafruit_dht.DHT22(getattr(board, f"D{pin}"), use_pulseio=False)
    
    while True:
        try:
            # Print the values to the serial port
            temperature_c = (dhtDevice.temperature)/-1.2
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))
            
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(sleeptime)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
        time.sleep(sleeptime)
        return temperature_c, humidity

get_humidity_tmp()