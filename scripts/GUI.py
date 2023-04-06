import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import sys
import random
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from client import ClientSocket
import queue

"""
# TODO
* Json files - The keys are days? why not showing the last 7 samples by date?
* Do we want the ability to change the graphs between weeks/month?
"""


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

        self.load_data()
        self.create_gui()

    def plot_food_consuming(self):
        # with open("../data/dog_water_consumption.json", "r") as f:
        #     data = json.load(f)

        # Create a list of x and y values for the plot
        x_values = list(self.food_weight_d.keys())
        y_values = list(self.food_weight_d.values())

        # Plot the data as a line graph
        plt.figure()
        plt.plot(x_values[:-7], y_values[:-7])
        plt.xlabel("Day of the week")
        plt.ylabel("Water consumption (liters)")
        plt.title("Dog water consumption over time")
        plt.show()

    def plot_water_consuming(self):
        # with open("../data/dog_food_consumption.json", "r") as f:
        #     data = json.load(f)

        # Create a list of x and y values for the plot
        # FIXME change the plot only to the wanted amount of points
        x_values = list(self.water_weight_d.keys())
        y_values = list(self.water_weight_d.values())

        # Plot the data as a line graph
        plt.figure()
        plt.plot(x_values[:-7], y_values[:-7])
        plt.xlabel("Day of the week")
        plt.ylabel("Food consumption (kilograms)")
        plt.title("Dog food consumption over time")
        plt.show()

    def plot_humidity(self):
        # with open("../data/dog_humidity.json", "r") as f:
        #     data = json.load(f)

        # Create a list of x and y values for the plot
        x_values = list(self.dog_house_humidity_d.keys())
        y_values = list(self.dog_house_humidity_d.values())

        # Plot the data as a line graph
        plt.figure()
        plt.plot(x_values[:-7], y_values[:-7])
        plt.xlabel("Day of the week")
        plt.ylabel("Dog House Humidity")
        plt.title("DogHouse Humidity Over Time")
        plt.show()

    def plot_dog_weight(self):  # for dog weight graph
        # with open("../data/dog_weights.json", "r") as f:
        #     data = json.load(f)

        # Create a list of x and y values for the plot
        x_values = list(self.dog_weight_d.keys())
        y_values = list(self.dog_weight_d.values())

        # Plot the data as a line graph
        plt.figure()
        plt.plot(x_values[:-7], y_values[:-7])
        plt.xlabel("Day")
        plt.ylabel("Dog Weight")
        plt.title("Dog Weight Over Time")
        plt.show()

    def plot_doghouse_temperature(self):  # for doghouse temperature
        with open("../data/dog_temperatures.json", "r") as f:
            data = json.load(f)

        # Create a list of x and y values for the plot
        x_values = list(data.keys())
        y_values = list(data.values())

        # Plot the data as a line graph
        plt.figure()
        plt.plot(x_values[:-7], y_values[:-7])
        plt.xlabel("Day of the week")
        plt.ylabel("Dog house temperature")
        plt.title("DogHouse Temperature Over Time")
        plt.show()

    def plot_water_temperature(self):  # for water temperature graph
        # Read data from the JSON file
        with open("../data/water_temp.json", "r") as infile:
            data = json.load(infile)

        # Extract dates and values from the data
        dates = [datetime.datetime.strptime(item["date"], "%Y-%m-%d %H:%M:%S") for item in data]
        values = [item["value"] for item in data]

        # Create a line plot of the data
        fig, ax = plt.subplots()
        ax.plot(dates, values)

        # Format the x-axis with a date scale
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        ax.xaxis.set_minor_locator(mdates.DayLocator())
        ax.tick_params(axis='x', rotation=45)

        # Set the title and axis labels
        ax.set_title("Water Temperature")
        ax.set_xlabel("Date")
        ax.set_ylabel("Temperature (C)")

        # Show the plot
        plt.show()

    def generate_values(self):
        self.dog_house_temp = round(random.uniform(10, 30), 2)
        self.dog_house_humidity = round(random.uniform(20, 80), 2)
        self.water_weight = round(random.uniform(0, 15), 2)
        self.water_temp = round(random.uniform(5, 15), 2)
        self.food_weight = round(random.uniform(0, 20), 2)
        self.dog_weight = round(random.uniform(5, 50), 2)

    def dog_house_temp_gen(self):
        print(f"Currently DogHouse Temperature: {self.dog_house_temp}°C, Humidity: {self.dog_house_humidity}%")
        # self.generate_values()

    def dog_house_hum_gen(self):
        print(f"Humidity: {self.dog_house_humidity}%")
        # self.generate_values()

    def water_temp_gen(self):
        print(f"Water Temperature: {self.water_temp}°C")
        # self.generate_values()

    def food_weight_gen(self):
        print(f"Food Tank Weight: {self.food_weight}Kg")
        # self.generate_values()

    def water_weight_gen(self):
        print(f"Water Tank Weight: {self.water_weight}L")
        # self.generate_values()

    def dog_weight_gen(self):
        print(f"Dog Weight: {self.dog_weight}Kg")
        # self.generate_values()

    def generate_random_data(self):
        # Generate 20 measurements for "Water Temperature" Graph
        data = {}
        start_date = datetime.datetime(2023, 2, 1)
        end_date = datetime.datetime(2023, 5, 31)
        for i in range(20):
            temperature = round(random.uniform(15, 25), 2)
            date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
            measurement = {date.strftime("%d/%m/%Y %H:%M:%S"): temperature}
            data.update(measurement)
        sorted_data = {k: v for k, v in
                       sorted(data.items(), key=lambda item: datetime.datetime.strptime(item[0], "%d/%m/%Y %H:%M:%S"))}
        self.water_temp_d = sorted_data

        # FIXME dates same as Water Temperature
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        for day in days:
            # Generate data for "Dog Weight" Graph
            self.dog_weight_d[day] = round(random.uniform(30, 35), 2)
            # Generate data for "Doghouse Temperature"
            self.dog_house_temp_d[day] = round(random.uniform(5, 35), 2)
            # Generate dog house humidity data
            self.dog_house_humidity_d[day] = round(random.uniform(20, 80), 2)
            # Generate dog food consumption data
            self.food_weight_d[day] = round(random.uniform(0.5, 2.5), 2)
            # Generate dog water consumption data
            self.water_weight_d[day] = round(random.uniform(0.5, 2.5), 2)

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
        with open("../data/water_temp.json", "r") as f:
            data = json.load(f)

        # FIXME need to do this to all the files after changing from day to dates
        for key in data:
            datetime_key = datetime.datetime.strptime(key, "%d/%m/%Y %H:%M:%S")
            self.water_temp_d[datetime_key] = data[key]

        with open("../data/dog_weights.json", "r") as f:
            self.dog_weight_d = json.load(f)

        with open("../data/dog_temperatures.json", "r") as f:
            self.water_temp_d = json.load(f)

        with open("../data/dog_humidity.json", "r") as f:
            self.dog_house_humidity_d = json.load(f)

        with open("../data/dog_water_consumption.json", "r") as f:
            self.water_weight_d = json.load(f)

        with open("../data/dog_food_consumption.json", "r") as f:
            self.food_weight_d = json.load(f)

    def update_status(self):
        self.temp_status.config(text=f"{self.dog_house_temp}")
        self.humid_status.config(text=f"{self.dog_house_humidity}")
        self.water_temp_status.config(text=f"{self.water_temp}")
        self.food_weight_status.config(text=f"{self.food_weight}")
        self.water_weight_status.config(text=f"{self.water_weight}")
        self.dog_weight_status.config(text=f"{self.dog_weight}")

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
        self.root.geometry("700x550")
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
        self.temp_status = tk.Label(stat_frame, text=f"{self.dog_house_temp}", **button_style, pady=10)
        self.temp_status.grid(row=1, column=0, sticky=tk.W + tk.E)

        humid_label = tk.Label(stat_frame, text="DogHouse\nHumidity", **label_style, pady=50)
        humid_label.grid(row=2, column=0, sticky=tk.W + tk.E)
        self.humid_status = tk.Label(stat_frame, text=f"{self.dog_house_humidity}", **button_style, pady=10)
        self.humid_status.grid(row=3, column=0, sticky=tk.W + tk.E)

        water_temp_label = tk.Label(stat_frame, text="Water\nTemperature", **label_style, pady=50)
        water_temp_label.grid(row=0, column=1, sticky=tk.W + tk.E)
        self.water_temp_status = tk.Label(stat_frame, text=f"{self.water_temp}", **button_style, pady=10)
        self.water_temp_status.grid(row=1, column=1, sticky=tk.W + tk.E)

        food_weight_label = tk.Label(stat_frame, text="Food\nTank`s Weight", **label_style, pady=50)
        food_weight_label.grid(row=0, column=2, sticky=tk.W + tk.E)
        self.food_weight_status = tk.Label(stat_frame, text=f"{self.food_weight}", **button_style, pady=10)
        self.food_weight_status.grid(row=1, column=2, sticky=tk.W + tk.E)

        water_weight_label = tk.Label(stat_frame, text="Water\nTank`s Weight", **label_style, pady=50)
        water_weight_label.grid(row=2, column=2, sticky=tk.W + tk.E)
        self.water_weight_status = tk.Label(stat_frame, text=f"{self.water_weight}", **button_style, pady=10)
        self.water_weight_status.grid(row=3, column=2, sticky=tk.W + tk.E)

        dog_weight_label = tk.Label(stat_frame, text="Dog\nWeight", **label_style, pady=50)
        dog_weight_label.grid(row=2, column=1, sticky=tk.W + tk.E)
        self.dog_weight_status = tk.Label(stat_frame, text=f"{self.dog_weight}", **button_style, pady=10)
        self.dog_weight_status.grid(row=3, column=1, sticky=tk.W + tk.E)

        stat_frame.pack(fill='x')

        plot_label = tk.Label(self.root, text="Graphs", **label_style)
        plot_label.pack(pady=10)

        graph_frame = tk.Frame(self.root)
        graph_frame.columnconfigure(0, weight=2)
        graph_frame.columnconfigure(1, weight=2)
        graph_frame.columnconfigure(2, weight=2)

        # pack the first row of buttons
        weight_graph_button = tk.Button(graph_frame, text="Dog Weight Graph", command=lambda: self.plot_dog_weight(),
                                        **button_style2, pady=10)
        weight_graph_button.grid(row=0, column=0, sticky=tk.W + tk.E)

        temp_graph_button = tk.Button(graph_frame, text="DogHouse Temperature Graph",
                                      command=lambda: self.plot_doghouse_temperature(),
                                      **button_style2, pady=10)
        temp_graph_button.grid(row=0, column=1, sticky=tk.W + tk.E)

        hum_graph_button = tk.Button(graph_frame, text="DogHouse Humidity Graph", command=lambda: self.plot_humidity(),
                                     **button_style2, pady=10)
        hum_graph_button.grid(row=0, column=2, sticky=tk.W + tk.E)

        # pack the second row of buttons
        water_graph_button = tk.Button(graph_frame, text="Water Consuming Graph",
                                       command=lambda: self.plot_water_consuming(),
                                       **button_style2, pady=10)
        water_graph_button.grid(row=1, column=0, sticky=tk.W + tk.E)

        food_graph_button = tk.Button(graph_frame, text="Food Consuming Graph",
                                      command=lambda: self.plot_food_consuming(),
                                      **button_style2, pady=10)
        food_graph_button.grid(row=1, column=1, sticky=tk.W + tk.E)

        temp_graph_button = tk.Button(graph_frame, text="Water Temperature Graph",
                                      command=lambda: self.plot_water_temperature(),
                                      **button_style2, pady=10)
        temp_graph_button.grid(row=1, column=2, sticky=tk.W + tk.E)

        graph_frame.pack(fill='x')

    def run(self):
        self.root.after(100, self.update_data)
        self.root.mainloop()


if __name__ == "__main__":
    client = ClientSocket("10.100.102.5")
    app = DogHouseApp(client)
    try:
        app.run()
    finally:
        app.dump_data()
        app.client_socket.dump_data()
        print("Closing")
