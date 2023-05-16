import socket
import json
import os
from datetime import datetime
import queue
import threading


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
