import time
import board
import adafruit_dht
 
# Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT22(board.D4)
 
# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.

def config_humidity_tmp(pin = 22, sleeptime = 2.0):
    print("Starting to config the humidity_tmp") 
    dhtDevice = adafruit_dht.DHT22(getattr(board, f"D{pin}"), use_pulseio=False)
    print("Done to config the humidity_tmp") 
    return dhtDevice

# Variable: pin(def=17), sleeptime(def=2.0)
def get_humidity_tmp(dhtDevice, pin = 22, sleeptime = 2.0):

    temperature_c, humidity = None, None
    while (not temperature_c or not humidity):
        try:
            # Print the values to the serial port
            temperature_c = -(dhtDevice.temperature)/-1.2
            humidity = dhtDevice.humidity
            
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(sleeptime)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
        
        time.sleep(sleeptime)
    print("Temp: {:.1f} C    Humidity: {}% ".format(temperature_c, humidity))
    return temperature_c, humidity


if "__main__" == __name__:
    dhtDevice = config_humidity_tmp()
    while(1):
        get_humidity_tmp(dhtDevice=dhtDevice)