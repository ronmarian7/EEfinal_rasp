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

class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, message):
        self.text_space.insert(tk.END, message)
    
def get_water_temperature(): # for water temeperature graph
    # Read data from the JSON file
    with open("water_temp.json", "r") as infile:
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

def generate_values():
    global dog_house_temp, dog_house_humidity, water_temp, food_weight, dog_weight
    dog_house_temp = round(random.uniform(10, 30), 2)
    dog_house_humidity = round(random.uniform(20, 80), 2)
    water_temp = round(random.uniform(5, 15), 2)
    food_weight = round(random.uniform(100, 500), 2)
    dog_weight = round(random.uniform(5, 50), 2)

    # Update the GUI elements to display the new values
    # temp_humid_label.config(text=f"Currently DogHouse Temperature: {dog_house_temp}°C, Humidity: {dog_house_humidity}%")
    # water_temp_label.config(text=f"Water Temperature: {water_temp}")
    # food_weight_label.config(text=f"Food Weight: {food_weight}")
    # dog_weight_label.config(text=f"Dog Weight: {dog_weight}")


def dog_house_temp_gen():
     print(f"Currently DogHouse Temperature: {dog_house_temp}°C, Humidity: {dog_house_humidity}%" )
     generate_values()
def water_temp_gen():
     print(f"Water Temperature: {water_temp}°C" )
     generate_values()
def food_weight_gen():
     print(f"Food Tank Weight: {food_weight}Kg" )
     generate_values()
def dog_weight_gen():
     print(f"Dog Weight: {dog_weight}Kg")
     generate_values()



dog_house_temp = round(random.uniform(10, 30), 2)
dog_house_humidity = round(random.uniform(20, 80), 2)
water_temp = round(random.uniform(5, 15), 2)
food_weight = round(random.uniform(100, 500), 2)
dog_weight = round(random.uniform(5, 50), 2)

# Generate 20 measurements for "Water Temperature" metric

data = []
start_date = datetime.datetime(2023, 2, 1)
end_date = datetime.datetime(2023, 5, 31)

for i in range(20):
    temperature = round(random.uniform(15, 25), 2)
    date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
    measurement = {"date": date.strftime("%Y-%m-%d %H:%M:%S"), "value": temperature}
    data.append(measurement)

data = sorted(data, key=lambda x: x['date'])


# Write data to a JSON file
with open("water_temp.json", "w") as outfile:
    json.dump(data, outfile)
    
# Define the GUI window
root = tk.Tk()
root.title("Smart Dog House - GUI")
root.geometry("700x550")
root.resizable(False, False)
root.configure(bg="white")  # Change background color to white

root2 = tk.Tk() #For outputs
root2.title("GUI outputs")
root2.geometry("600x300")

text_widget = tk.Text(root2)
text_widget.pack() 
sys.stdout = StdoutRedirector(text_widget) # Redirect output to widget instead of terminal

# Load the image
image_path = r"C:\Users\Liron\Desktop\Smart DogHouse\EEfinal_rasp\Picture\del_pic.jpg"
image = Image.open(image_path)



# Resize the image to fit the GUI
image = image.resize((900, 900), Image.ANTIALIAS)

# Convert the image to a Tkinter PhotoImage and set it as the background
photo = ImageTk.PhotoImage(image)
background_label = tk.Label(root, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


# Define styles for labels and buttons
label_style = {"font": ("Arial", 16, "bold"), "fg": "black", "bg": "white"}  # Change label color to black and background color to white
button_style = {"font": ("Arial", 12), "fg": "white", "bg": "#0074D9"}  # Change button color to blue
label_style2 = {"font": ("Arial", 16, "bold"), "fg": "black"} 
# Define the labels and buttons
temp_humid_label = tk.Label(root, text="DogHouse Temperature & Humidity", **label_style)
temp_humid_label.pack(pady=10)
temp_humid_button = tk.Button(root, text="Check", command=dog_house_temp_gen, **button_style)
temp_humid_button.pack()

water_temp_label = tk.Label(root, text="Water Temperature", **label_style)
water_temp_label.pack(pady=10)
water_temp_button = tk.Button(root, text="Check", command=water_temp_gen, **button_style)
water_temp_button.pack()

food_weight_label = tk.Label(root, text="Food Weight", **label_style)
food_weight_label.pack(pady=10)
food_weight_button = tk.Button(root, text="Check",command= food_weight_gen, **button_style)
food_weight_button.pack()



dog_weight_label = tk.Label(root, text="Dog Weight", **label_style)
dog_weight_label.pack(pady=10)
dog_weight_button = tk.Button(root, text="Check", command= dog_weight_gen, **button_style)
dog_weight_button.pack()

generate_button = tk.Button(root, text="Generate Values", command=generate_values) 


row1 = tk.Frame(root)
row2 = tk.Frame(root)

# pack the first row of buttons
weight_graph_button = tk.Button(row1, text="Dog Weight Graph", command=lambda: print("Weight Graph"), **button_style)
weight_graph_button.pack(side='left', padx=0, pady=0)

temp_graph_button = tk.Button(row1, text="DogHouse Temperature Graph", command=lambda: print("Temperature Graph"), **button_style)
temp_graph_button.pack(side='left', padx=0, pady=0)

hum_graph_button = tk.Button(row1, text="DogHouse Humidity Graph", command=lambda: print("Humidity Graph"), **button_style)
hum_graph_button.pack(side='left', padx=0, pady=0)

# pack the second row of buttons
water_graph_button = tk.Button(row2, text="Water Consuming Graph", command=lambda: print("Water Graph"), **button_style)
water_graph_button.pack(side='left', padx=0, pady=0.5)

food_graph_button = tk.Button(row2, text="Food Consuming Graph", command=lambda: print("Food Graph"), **button_style)
food_graph_button.pack(side='left', padx=0, pady=0.5)

temp_graph_button = tk.Button(row2, text="Water Temperature Graph", command=lambda: get_water_temperature(), **button_style)
temp_graph_button.pack(side='left', padx=0, pady=0.5)

# pack the rows of buttons into the main window
plot_label = tk.Label(root, text="Graphs",**label_style2)
plot_label.pack(pady=60)

row1.pack()
row2.pack()
generate_button.pack()

# Define the plot window for the graphs
fig = Figure(figsize=(6, 4), dpi=100)
plot_window = FigureCanvasTkAgg(fig, root)
plot_window.get_tk_widget().pack(padx=20, pady=10, side=tk.BOTTOM, fill=tk.BOTH, expand=1)

#if(not(root2.winfo_exists())):
 #   root2 = tk.Tk() #For outputs
root.mainloop()
