import tkinter as tk
import json
import random
import matplotlib.pyplot as plt
from client import ClientSocket
import queue
import os


class DogHouseApp:
    def __init__(self, client_socket: ClientSocket):
        self.client_socket = client_socket
        self.root = tk.Tk()

        self.dog_house_temp_d = {}
        self.dog_house_humidity_d = {}
        self.water_temp_d = {}
        self.food_weight_d = {}
        self.dog_weight_d = {}
        self.water_weight_d = {}

        self.time = None
        self.dog_house_temp = 0
        self.dog_house_humidity = 0
        self.water_temp = 0
        self.food_weight = 0
        self.dog_weight = 0
        self.water_weight = 0

        self.temp_status = None
        self.humid_status = None
        self.water_temp_status = None
        self.food_weight_status = None
        self.water_weight_status = None
        self.dog_weight_status = None

        self.num_samp2plot = 60

        self.load_data()
        self.create_gui()

    def plot(self, data_dict, title: str):
        # Create a list of x and y values for the plot
        x_values = list(data_dict.keys())
        y_values = list(data_dict.values())

        # Plot the data as a line graph
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_values[-self.num_samp2plot:], y_values[-self.num_samp2plot:])

        # Filter x-axis labels to only include the first label of each minute
        x_ticks = [x_values[-self.num_samp2plot][0]]
        for label in x_values[-self.num_samp2plot:]:
            if label[14:16] != x_ticks[-1][14:16]:
                x_ticks.append(label)

        # Format the x-axis tick labels to display the date and hour only
        formatted_x = [label[:5] + '\n' + label[10:-3] for label in x_ticks]
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(formatted_x)

        ax.set_xlabel("Samples")
        ax.set_ylabel(f"Dog {title}")
        ax.set_title(f"Dog {title} Over Time")

        # Adjust x-axis limits to show all the plotted data
        ax.set_xlim(left=x_values[-self.num_samp2plot], right=x_values[-1])
        plt.show()

    def generate_values(self):
        self.dog_house_temp = round(random.uniform(10, 30), 2)
        self.dog_house_humidity = round(random.uniform(20, 80), 2)
        self.water_weight = round(random.uniform(0, 15), 2)
        self.water_temp = round(random.uniform(5, 15), 2)
        self.food_weight = round(random.uniform(0, 20), 2)
        self.dog_weight = round(random.uniform(5, 50), 2)

    def get_dog_house_temp(self):
        print(f"Currently DogHouse Temperature: {self.dog_house_temp}°C, Humidity: {self.dog_house_humidity}%")

    def get_dog_house_hum(self):
        print(f"Humidity: {self.dog_house_humidity}%")

    def get_water_temp(self):
        print(f"Water Temperature: {self.water_temp}°C")

    def get_food_weight(self):
        print(f"Food Tank Weight: {self.food_weight}Kg")

    def get_water_weight(self):
        print(f"Water Tank Weight: {self.water_weight}L")

    def get_dog_weight(self):
        print(f"Dog Weight: {self.dog_weight}Kg")

    def dump_data(self):
        # Write data to a JSON file
        with open("../data/water_temp.json", "w") as f:
            json.dump(self.water_temp_d, f)
        with open("../data/dog_weights.json", "w") as f:
            json.dump(self.dog_weight_d, f)
        with open("../data/dog_temperatures.json", "w") as f:
            json.dump(self.dog_house_temp_d, f)
        with open("../data/dog_humidity.json", "w") as f:
            json.dump(self.dog_house_humidity_d, f)
        with open("../data/dog_water_consumption.json", "w") as f:
            json.dump(self.water_weight_d, f)
        with open("../data/dog_food_consumption.json", "w") as f:
            json.dump(self.food_weight_d, f)

    def load_data(self):
        # load data to a JSON file
        if os.path.exists("../data/water_temp.json"):
            print("Loading Json Data")
            with open("../data/water_temp.json", "r") as f:
                self.water_temp_d = json.load(f)

            with open("../data/dog_weights.json", "r") as f:
                self.dog_weight_d = json.load(f)

            with open("../data/dog_temperatures.json", "r") as f:
                self.dog_house_temp_d = json.load(f)

            with open("../data/dog_humidity.json", "r") as f:
                self.dog_house_humidity_d = json.load(f)

            with open("../data/dog_water_consumption.json", "r") as f:
                self.water_weight_d = json.load(f)

            with open("../data/dog_food_consumption.json", "r") as f:
                self.food_weight_d = json.load(f)
        else:
            print("Can't find history Json Data")

    def update_status(self):
        self.temp_status.config(text=f"{self.dog_house_temp}°C")
        self.humid_status.config(text=f"{self.dog_house_humidity}%")
        self.water_temp_status.config(text=f"{self.water_temp}°C")
        self.food_weight_status.config(text=f"{self.food_weight}Kg")
        self.water_weight_status.config(text=f"{self.water_weight}L")
        self.dog_weight_status.config(text=f"{self.dog_weight}Kg")

    def update_data(self):
        try:
            data = self.client_socket.data_queue.get_nowait()
        except queue.Empty:
            pass
        else:
            splinted_data = data.split(',')
            self.time = splinted_data[0]
            data = [int(i) for i in splinted_data[1:]]
            self.dog_house_temp, self.dog_house_humidity, self.dog_weight, \
                self.food_weight, self.water_weight, self.water_temp = data

            self.update_status()

            self.dog_house_temp_d[self.time] = self.dog_house_temp
            self.dog_house_humidity_d[self.time] = self.dog_house_humidity
            self.water_temp_d[self.time] = self.water_temp
            self.food_weight_d[self.time] = self.food_weight
            self.dog_weight_d[self.time] = self.dog_weight
            self.water_weight_d[self.time] = self.water_weight

        self.root.after(1000, self.update_data)  # Update data every 1000 ms (1 second)

    def create_gui(self):

        # Define the GUI window
        self.root.title("Smart Dog House - GUI")
        self.root.geometry("700x535")
        # self.root.resizable(False, False)
        self.root.configure(bg="white")  # Change background color to white

        # Define styles for labels and buttons
        label_style = {"font": ("Arial", 16, "bold"), "fg": "black",
                       "bg": "white"}  # Change label color to black and background color to white
        button_style = {"font": ("Arial", 12), "fg": "white", "bg": "#0074D9"}  # Change button color to blue
        button_style2 = {"font": ("Arial", 13), "fg": "white", "bg": "#0074D9"}  # Change button color to blue
        label_style2 = {"font": ("Arial", 16, "bold"), "fg": "black"}
        # Define the labels and buttons

        stat_frame = tk.Frame(self.root)
        stat_frame.columnconfigure(0, weight=1)
        stat_frame.columnconfigure(1, weight=1)
        stat_frame.columnconfigure(2, weight=1)

        temp_label = tk.Label(stat_frame, text="DogHouse\nTemperature", **label_style, pady=50)
        temp_label.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.temp_status = tk.Label(stat_frame, text=f"{self.dog_house_temp}°C", **button_style, pady=10)
        self.temp_status.grid(row=1, column=0, sticky=tk.W + tk.E)

        humid_label = tk.Label(stat_frame, text="DogHouse\nHumidity", **label_style, pady=50)
        humid_label.grid(row=2, column=0, sticky=tk.W + tk.E)
        self.humid_status = tk.Label(stat_frame, text=f"{self.dog_house_humidity}%", **button_style, pady=10)
        self.humid_status.grid(row=3, column=0, sticky=tk.W + tk.E)

        water_temp_label = tk.Label(stat_frame, text="Water\nTemperature", **label_style, pady=50)
        water_temp_label.grid(row=0, column=1, sticky=tk.W + tk.E)
        self.water_temp_status = tk.Label(stat_frame, text=f"{self.water_temp}°C", **button_style, pady=10)
        self.water_temp_status.grid(row=1, column=1, sticky=tk.W + tk.E)

        food_weight_label = tk.Label(stat_frame, text="Food\nTank`s Weight", **label_style, pady=50)
        food_weight_label.grid(row=0, column=2, sticky=tk.W + tk.E)
        self.food_weight_status = tk.Label(stat_frame, text=f"{self.food_weight}KG", **button_style, pady=10)
        self.food_weight_status.grid(row=1, column=2, sticky=tk.W + tk.E)

        water_weight_label = tk.Label(stat_frame, text="Water\nTank`s Weight", **label_style, pady=50)
        water_weight_label.grid(row=2, column=2, sticky=tk.W + tk.E)
        self.water_weight_status = tk.Label(stat_frame, text=f"{self.water_weight}KG", **button_style, pady=10)
        self.water_weight_status.grid(row=3, column=2, sticky=tk.W + tk.E)

        dog_weight_label = tk.Label(stat_frame, text="Dog\nWeight", **label_style, pady=50)
        dog_weight_label.grid(row=2, column=1, sticky=tk.W + tk.E)
        self.dog_weight_status = tk.Label(stat_frame, text=f"{self.dog_weight}KG", **button_style, pady=10)
        self.dog_weight_status.grid(row=3, column=1, sticky=tk.W + tk.E)

        stat_frame.pack(fill='x')

        plot_label = tk.Label(self.root, text="Graphs", **label_style)
        plot_label.pack(pady=10)

        graph_frame = tk.Frame(self.root)
        graph_frame.columnconfigure(0, weight=2)
        graph_frame.columnconfigure(1, weight=2)
        graph_frame.columnconfigure(2, weight=2)

        # pack the first row of buttons
        weight_graph_button = tk.Button(graph_frame, text="Dog Weight Graph",
                                        command=lambda: self.plot(data_dict=self.dog_weight_d, title="Weight"),
                                        **button_style2, pady=10)
        weight_graph_button.grid(row=0, column=0, sticky=tk.W + tk.E)

        temp_graph_button = tk.Button(graph_frame, text="DogHouse Temperature Graph",
                                      command=lambda: self.plot(data_dict=self.dog_house_temp_d, title="Temperature"),
                                      **button_style2, pady=10)
        temp_graph_button.grid(row=0, column=1, sticky=tk.W + tk.E)

        hum_graph_button = tk.Button(graph_frame, text="DogHouse Humidity Graph",
                                     command=lambda: self.plot(data_dict=self.dog_house_humidity_d, title="Humidity"),
                                     **button_style2, pady=10)
        hum_graph_button.grid(row=0, column=2, sticky=tk.W + tk.E)

        water_graph_button = tk.Button(graph_frame, text="Water Consuming Graph",
                                       command=lambda: self.plot(data_dict=self.water_weight_d,
                                                                 title="Water Consuming"),
                                       **button_style2, pady=10)
        water_graph_button.grid(row=1, column=0, sticky=tk.W + tk.E)

        food_graph_button = tk.Button(graph_frame, text="Food Consuming Graph",
                                      command=lambda: self.plot(data_dict=self.food_weight_d, title="Food Consuming"),
                                      **button_style2, pady=10)
        food_graph_button.grid(row=1, column=1, sticky=tk.W + tk.E)

        temp_graph_button = tk.Button(graph_frame, text="Water Temperature Graph",
                                      command=lambda: self.plot(data_dict=self.water_temp_d, title="Water Temperature"),
                                      **button_style2, pady=10)
        temp_graph_button.grid(row=1, column=2, sticky=tk.W + tk.E)

        graph_frame.pack(fill='x')

    def run(self):
        self.root.after(100, self.update_data)
        self.root.mainloop()


if __name__ == "__main__":
    client = ClientSocket("192.168.1.130")
    app = DogHouseApp(client)
    try:
        app.run()
    finally:
        app.dump_data()
        app.client_socket.dump_data()
        print("Closing")
