import socket
import json
import os
import threading

"""
TODOs
1. need to add an interface for the gui
2. need to add an interface for the data processing  
3. the socket_server and all the other data processing needs to be in different thread 
"""


class ClientSocket:
    def __init__(self, lock: threading.Lock, HOST: str, PORT: int = 65432):
        self.lock = lock
        self.area_temperature_d = {}
        self.area_humidity_d = {}
        self.dog_weight_d = {}
        self.food_weight_d = {}
        self.water_weight_d = {}
        self.water_temperature_d = {}
        self.HOST = HOST
        self.PORT = PORT

    def load_data(self):
        # if this file exists then we can assume that all the other files exists
        if os.path.exists("data\\area_temperature.json"):
            with open("data\\area_temperature.json", "r") as f:
                self.area_temperature_d = json.load(f)
            with open("data\\area_humidity.json", "r") as f:
                self.area_humidity_d = json.load(f)
            with open("data\\dog_weight.json", "r") as f:
                self.dog_weight_d = json.load(f)
            with open("data\\food_weight.json", "r") as f:
                self.food_weight_d = json.load(f)
            with open("data\\water_weight.json", "r") as f:
                self.water_weight_d = json.load(f)
            with open("data\\water_temperature.json", "r") as f:
                self.water_temperature_d = json.load(f)

    def dump_data(self):
        with open("data\\area_temperature.json", "w") as f:
            json.dump(self.area_temperature_d, f, indent="")
        with open("data\\area_humidity.json", "w") as f:
            json.dump(self.area_humidity_d, f, indent="")
        with open("data\\dog_weight.json", "w") as f:
            json.dump(self.dog_weight_d, f, indent="")
        with open("data\\food_weight.json", "w") as f:
            json.dump(self.food_weight_d, f, indent="")
        with open("data\\water_weight.json", "w") as f:
            json.dump(self.water_weight_d, f, indent="")
        with open("data\\water_temperature.json", "w") as f:
            json.dump(self.water_temperature_d, f, indent="")

    def run_client(self):
        self.lock.acquire()
        self.load_data()
        self.lock.release()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                print(f"Trying to connect to HOST: {self.HOST}, PORT: {self.PORT}")
                s.connect((self.HOST, self.PORT))
                print(f"connected to HOST: {self.HOST}, PORT: {self.PORT}")
                while True:
                    # Receive data from the socket connection
                    data = s.recv(1024).decode()
                    # Check if there are 6 commas (and 7 elements) before splitting the string
                    assert data.count(",") == 6, "Error: Data string does not have the expected number of elements."
                    # process the data to variables
                    time, area_temperature, area_humidity, dog_weight, food_weight, \
                        water_weight, water_temperature = data.split(',')

                    print(f"Time {time}")
                    self.lock.acquire()
                    print(f"Area_temperature {area_temperature}")
                    self.area_temperature_d[time] = area_temperature

                    print(f"Area_humidity {area_humidity}")
                    self.area_humidity_d[time] = area_humidity

                    print(f"Dog_weight {dog_weight}")
                    if dog_weight > 2:  # Not empty doghouse
                        self.dog_weight_d[time] = dog_weight

                    print(f"Food_weight {food_weight}")
                    self.food_weight_d[time] = food_weight

                    print(f"Water_weight {water_weight}")
                    self.water_weight_d[time] = water_weight

                    print(f"Water_temperature {water_temperature}")
                    self.water_temperature_d[time] = water_temperature

                    # Get the last ten values from the dictionary
                    last_ten_values = [int(value) for key, value in list(self.dog_weight_d.items())[-10:]]
                    # Calculate the average of the last ten values
                    average_weight = sum(last_ten_values) / len(last_ten_values)

                    self.lock.release()

                    # Check if the values meet out requirements
                    # FIXME need to see if we need to check the values of the other sensors also
                    if not (0.9 * average_weight <= dog_weight <= 1.1 * average_weight):
                        pass
                    if not (10 <= area_temperature <= 50): # FIXME - weight of the doghouse
                        pass
                    if not (0.5 <= water_weight): # FIXME - weight of the dispense
                        pass
                    if not (3 <= food_weight):  # FIXME - weight of the dispenser
                        pass

            except KeyboardInterrupt:
                print("Session ended by the user")
            except Exception as e:
                raise e
            finally:
                self.lock.acquire()
                self.dump_data()
                self.lock.release()


if __name__ == "__main__":
    client = ClientSocket(lock=threading.Lock(), HOST="1.1.1.1")
    client.run_client()
