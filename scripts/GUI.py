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
import threading

"""
# TODO
* Add a lock for multi threading and see what are the shared variables 
* Json files - The keys are days? why not showing the last 7 samples by date?
* Do we want the ability to change the graphs between weeks/month?
* After changing the code the background is not showing - need to fix  
* *_gen functions - why do we generate after printing and not before?
    later we will be using real date
    ** Why do we generate for all the sensors and not only for the wanted one?
* There is alot of space between the Graphs title and the buttons  
* Need to be sync about the names of the files and variables  
"""

class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, message):
        self.text_space.insert(tk.END, message)

    def flush(self):
        pass  # Add a flush method that does nothing


class DogHouseApp:
    def __init__(self, lock: threading.Lock):
        self.lock = lock  # TODO
        self.root = tk.Tk()
        self.root2 = tk.Tk()  # For outputs
        self.dog_house_temp = round(random.uniform(10, 30), 2)
        self.dog_house_humidity = round(random.uniform(20, 80), 2)
        self.water_temp = round(random.uniform(5, 15), 2)
        self.food_weight = round(random.uniform(0, 20), 2)
        self.dog_weight = round(random.uniform(5, 50), 2)
        self.water_weight = round(random.uniform(0, 20), 2)

        self.create_gui()

    def plot_food_consuming(self):
        with open("../data/dog_water_consumption.json", "r") as f:
            data = json.load(f)

        # Create a list of x and y values for the plot
        x_values = list(data.keys())
        y_values = list(data.values())

        # Plot the data as a line graph
        plt.figure()
        plt.plot(x_values, y_values)
        plt.xlabel("Day of the week")
        plt.ylabel("Water consumption (liters)")
        plt.title("Dog water consumption over time")
        plt.show()

    def plot_water_consuming(self):
        with open("../data/dog_food_consumption.json", "r") as f:
            data = json.load(f)

        # Create a list of x and y values for the plot
        x_values = list(data.keys())
        y_values = list(data.values())

        # Plot the data as a line graph
        plt.figure()
        plt.plot(x_values, y_values)
        plt.xlabel("Day of the week")
        plt.ylabel("Food consumption (kilograms)")
        plt.title("Dog food consumption over time")
        plt.show()

    def plot_humidity(self):
        with open("../data/dog_humidity.json", "r") as f:
            data = json.load(f)

        # Create a list of x and y values for the plot
        x_values = list(data.keys())
        y_values = list(data.values())

        # Plot the data as a line graph
        plt.figure()
        plt.plot(x_values, y_values)
        plt.xlabel("Day of the week")
        plt.ylabel("Dog House Humidity")
        plt.title("DogHouse Humidity Over Time")
        plt.show()

    def plot_dog_weight(self):  # for dog weight graph
        with open("../data/dog_weights.json", "r") as f:
            data = json.load(f)
        # Create a list of x and y values for the plot
        x_values = list(data.keys())
        y_values = list(data.values())

        # Plot the data as a line graph
        plt.figure()
        plt.plot(x_values, y_values)
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
        plt.plot(x_values, y_values)
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
        self.generate_values()

    def water_temp_gen(self):
        print(f"Water Temperature: {self.water_temp}°C")
        self.generate_values()

    def food_weight_gen(self):
        print(f"Food Tank Weight: {self.food_weight}Kg, Water Tank Weight: {self.water_weight}L")
        self.generate_values()

    def dog_weight_gen(self):
        print(f"Dog Weight: {self.dog_weight}Kg")
        self.generate_values()

    def generate_random_data(self):
        # Generate 20 measurements for "Water Temperature" Graph
        data = []
        start_date = datetime.datetime(2023, 2, 1)
        end_date = datetime.datetime(2023, 5, 31)
        for i in range(20):
            temperature = round(random.uniform(15, 25), 2)
            date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
            measurement = {"date": date.strftime("%Y-%m-%d %H:%M:%S"), "value": temperature}
            data.append(measurement)
        data = sorted(data, key=lambda x: x['date'])
        # Generate data for "Dog Weight" Graph
        weights = {}
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        for day in days:
            weights[day] = round(random.uniform(30, 35), 2)
        # Generate data for "Doghouse Temperature"
        temperatures = {}
        for day in days:
            temperatures[day] = round(random.uniform(5, 35), 2)
        # Generate dog house humidity data
        humidity = {}
        for day in days:
            humidity[day] = round(random.uniform(20, 80), 2)
        # Generate dog food consumption data
        food_consumption = {}
        for day in days:
            food_consumption[day] = round(random.uniform(0.5, 2.5), 2)
        # Generate dog water consumption data
        water_consumption = {}
        for day in days:
            water_consumption[day] = round(random.uniform(0.5, 2.5), 2)
        # Write data to a JSON file
        with open("../data/water_temp.json", "w") as outfile:
            json.dump(data, outfile)
        with open("../data/dog_weights.json", "w") as f:
            json.dump(weights, f)
        with open("../data/dog_temperatures.json", "w") as f:
            json.dump(temperatures, f)
        with open("../data/dog_humidity.json", "w") as f:
            json.dump(humidity, f)
        with open("../data/dog_water_consumption.json", "w") as f:
            json.dump(water_consumption, f)
        with open("../data/dog_food_consumption.json", "w") as f:
            json.dump(food_consumption, f)

    def create_gui(self):
        self.generate_values()
        self.generate_random_data()

        # Define the GUI window
        self.root.title("Smart Dog House - GUI")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        self.root.configure(bg="white")  # Change background color to white

        self.root2.title("GUI outputs")
        self.root2.geometry("600x300")

        text_widget = tk.Text(self.root2)
        text_widget.pack()
        sys.stdout = StdoutRedirector(text_widget)  # Redirect output to widget instead of terminal

        # Load the image
        image_path = "../Picture/del_pic.jpg"
        image = Image.open(image_path)

        # Resize the image to fit the GUI
        image = image.resize((900, 900), Image.LANCZOS)

        # Convert the image to a Tkinter PhotoImage and set it as the background
        photo = ImageTk.PhotoImage(image)
        background_label = tk.Label(self.root, image=photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Define styles for labels and buttons
        label_style = {"font": ("Arial", 16, "bold"), "fg": "black",
                       "bg": "white"}  # Change label color to black and background color to white
        button_style = {"font": ("Arial", 12), "fg": "white", "bg": "#0074D9"}  # Change button color to blue
        label_style2 = {"font": ("Arial", 16, "bold"), "fg": "black"}
        # Define the labels and buttons
        temp_humid_label = tk.Label(self.root, text="DogHouse Temperature & Humidity", **label_style)
        temp_humid_label.pack(pady=10)
        temp_humid_button = tk.Button(self.root, text="Check", command=self.dog_house_temp_gen, **button_style)
        temp_humid_button.pack()

        water_temp_label = tk.Label(self.root, text="Water Temperature", **label_style)
        water_temp_label.pack(pady=10)
        water_temp_button = tk.Button(self.root, text="Check", command=self.water_temp_gen, **button_style)
        water_temp_button.pack()

        food_weight_label = tk.Label(self.root, text="Food & Water Tank`s Weight", **label_style)
        food_weight_label.pack(pady=10)
        food_weight_button = tk.Button(self.root, text="Check", command=self.food_weight_gen, **button_style)
        food_weight_button.pack()

        dog_weight_label = tk.Label(self.root, text="Dog Weight", **label_style)
        dog_weight_label.pack(pady=10)
        dog_weight_button = tk.Button(self.root, text="Check", command=self.dog_weight_gen, **button_style)
        dog_weight_button.pack()

        generate_button = tk.Button(self.root, text="Generate Values", command=self.generate_values)

        row1 = tk.Frame(self.root)
        row2 = tk.Frame(self.root)

        # pack the first row of buttons
        weight_graph_button = tk.Button(row1, text="Dog Weight Graph", command=lambda: self.plot_dog_weight(),
                                        **button_style)
        weight_graph_button.pack(side='left', padx=0, pady=0)

        temp_graph_button = tk.Button(row1, text="DogHouse Temperature Graph",
                                      command=lambda: self.plot_doghouse_temperature(),
                                      **button_style)
        temp_graph_button.pack(side='left', padx=0, pady=0)

        hum_graph_button = tk.Button(row1, text="DogHouse Humidity Graph", command=lambda: self.plot_humidity(),
                                     **button_style)
        hum_graph_button.pack(side='left', padx=0, pady=0)

        # pack the second row of buttons
        water_graph_button = tk.Button(row2, text="Water Consuming Graph", command=lambda: self.plot_water_consuming(),
                                       **button_style)
        water_graph_button.pack(side='left', padx=0, pady=0.5)

        food_graph_button = tk.Button(row2, text="Food Consuming Graph", command=lambda: self.plot_food_consuming(),
                                      **button_style)
        food_graph_button.pack(side='left', padx=0, pady=0.5)

        temp_graph_button = tk.Button(row2, text="Water Temperature Graph",
                                      command=lambda: self.plot_water_temperature(),
                                      **button_style)
        temp_graph_button.pack(side='left', padx=0, pady=0.5)

        # pack the rows of buttons into the main window
        plot_label = tk.Label(self.root, text="Graphs", **label_style2)
        plot_label.pack(pady=60)

        row1.pack()
        row2.pack()

        # Define the plot window for the graphs
        fig = Figure(figsize=(6, 4), dpi=100)
        plot_window = FigureCanvasTkAgg(fig, self.root)
        plot_window.get_tk_widget().pack(padx=20, pady=10, side=tk.BOTTOM, fill=tk.BOTH, expand=1)


if __name__ == "__main__":
    lock = threading.Lock()
    app = DogHouseApp(lock)
    app.root.mainloop()
