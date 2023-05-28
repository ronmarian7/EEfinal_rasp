import socket
import json
import os
from datetime import datetime
import queue
import threading
import tkinter as tk


class ClientSocket:
    def __init__(self, HOST: str, PORT: int = 65432):
        self.HOST = HOST
        self.PORT = PORT
        self.data_queue = queue.Queue()

        self.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.dog_weight = 0
        self.dog_house_temp = 0
        self.dog_house_humidity = 0
        self.food_weight = 0
        self.water_weight = 0
        self.water_temp = 0

        self.thread = threading.Thread(target=self.run_client, daemon=True)
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
        print("Time - {}  dog_house_temp: {:.1f} C    dog_house_humidity: {:.2f}%  dog_weight: {:.2f}KG    food_weight: {:.2f}gr\
               water_weight: {:.2f}ml    water_temperature: {:.2f}C".format(self.time, self.dog_house_temp,
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
                    data = s.recv(1024).decode()
                    if data:
                        if data.count(",") == 6:
                            splinted_data = data.split(',')
                            self.time = splinted_data[0]
                            try:
                                self.dog_house_temp, self.dog_house_humidity, self.dog_weight, self.food_weight, \
                                self.water_weight, self.water_temp = [float(i) for i in splinted_data[1:]]
                            except ValueError:
                                print("Error: Data received is not in the expected format.")
                                continue
                            self.print_data()
                            self.data_queue.put(data)
                        else:
                            print("Error: Data string does not have the expected number of elements.")
            except (ConnectionResetError, KeyboardInterrupt):
                print("Session ended by the user")
            except (socket.error, socket.gaierror) as e:
                print(f"Error: {e}")
            except Exception as e:
                raise e
            finally:
                s.close()


if __name__ == "__main__":
    client = ClientSocket(HOST="10.100.102.5")
