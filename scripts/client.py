import socket
import json
import os
from datetime import datetime
import queue
import threading
import tkinter as tk

"""
TODOs
1. need to add an interface for the gui
2. need to add an interface for the data processing  
3. the socket_server and all the other data processing needs to be in different thread 
"""


class ClientSocket:
    def __init__(self, HOST: str, PORT: int = 65432):
        # self.lock = lock
        self.HOST = HOST
        self.PORT = PORT
        self.data_queue = queue.Queue()

        self.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.num_samples = 0
        self.avg_dog_weight = 0

        self.dog_weight = 0
        self.dog_house_temp = 0
        self.dog_house_humidity = 0
        self.food_weight = 0
        self.water_weight = 0
        self.water_temp = 0

        self.thread = threading.Thread(target=self.run_client)
        self.thread.start()

    def load_data(self):
        if os.path.exists("../data/avg_client_data.json"):
            with open("../data/avg_client_data.json", "r") as f:
                data = json.load(f)
                self.avg_dog_weight = int(data["avg_dog_weight"])
                self.num_samples = int(data["num_samples"])

    def dump_data(self):
        with open("../data/avg_client_data.json", "w") as f:
            avg_client_data = {"avg_dog_weight": self.avg_dog_weight, "num_samples": self.num_samples}
            json.dump(avg_client_data, f, indent="")

    def calc_new_avg(self):
        if self.dog_weight > 2:  # threshold for the dog weight
            self.avg_dog_weight = ((self.avg_dog_weight * self.num_samples) + self.dog_weight) / (self.num_samples + 1)
            self.num_samples += 1
    

    def exceeding_requirements_printer(req_exceeded: str):
        root = tk.Tk()
        root.title("Alert")
        root.geometry("250x100")
    
        msg = tk.Label(root, text=f"{req_exceeded} Exceeded the requirements")
        msg.pack(pady=20)
        # TODO: make some sound alert also!
        ok_button = tk.Button(root, text="OK", command=root.destroy)
        ok_button.pack(pady=10)
    
        root.mainloop()

    def check_data(self):
        # Check if the values meet out requirements
        # FIXME need to see if we need to check the values of the other sensors also
        if self.dog_weight > 2:
            if not (0.9 * self.avg_dog_weight <= self.dog_weight <= 1.1 * self.avg_dog_weight):
                self.exceeding_requirements_printer("Dog Weight")
        if not (10 <= self.dog_house_temp <= 40):  # FIXME - weight of the doghouse
            self.exceeding_requirements_printer("Dog House Temperature")
        if not (0.5 <= self.water_weight):  # FIXME - weight of the dispense
            self.exceeding_requirements_printer("Water Weight")
        if not (3 <= self.food_weight):  # FIXME - weight of the dispenser
            self.exceeding_requirements_printer("Food Weight")

    def print_data(self):
        print("Time - {}  dog_house_temp: {:.1f} C    dog_house_humidity: {}%  dog_weight: {}KG    food_weight: {}gr\
               water_weight: {}ml    water_temperature: {}C".format(self.time, self.dog_house_temp,
                                                                    self.dog_house_humidity, self.dog_weight,
                                                                    self.food_weight, self.water_weight,
                                                                    self.water_temp))

    def run_client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                print(f"Trying to connect to HOST: {self.HOST}, PORT: {self.PORT}")
                s.connect((self.HOST, self.PORT))
                print(f"connected to HOST: {self.HOST}, PORT: {self.PORT}")
                while True:
                    # Receive data from the socket connection
                    data = s.recv(1024).decode()
                    # Check if there are 6 commas (and 7 elements) before splitting the string
                    if data:
                        assert data.count(",") == 6, "Error: Data string does not have the expected number of elements."

                        # process the data to variables
                        splinted_data = data.split(',')
                        self.time = splinted_data[0]
                        self.dog_house_temp, self.dog_house_humidity, self.dog_weight, self.food_weight, \
                            self.water_weight, self.water_temp = [int(i) for i in splinted_data[1:]]

                        # self.print_data()
                        self.check_data()
                        self.calc_new_avg()

                        self.data_queue.put(data)

            except KeyboardInterrupt:
                print("Session ended by the user")
            except Exception as e:
                raise e
            finally:
                self.dump_data()


if __name__ == "__main__":
    client = ClientSocket(HOST="10.100.102.5")
    client.run_client()
