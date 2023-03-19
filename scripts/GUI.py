import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define the GUI window
root = tk.Tk()
root.title("Smart Dog House")
root.geometry("650x550")
root.resizable(False, False)
root.configure(bg="white")  # Change background color to white

# Load the image
image_path = r"C:\Users\Liron\Desktop\Smart DogHouse\EEfinal_rasp\Picture\del_pic.jpg"
image = Image.open(image_path)

# Resize the image to fit the GUI
image = image.resize((650, 900), Image.ANTIALIAS)

# Convert the image to a Tkinter PhotoImage and set it as the background
photo = ImageTk.PhotoImage(image)
background_label = tk.Label(root, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)



# Define styles for labels and buttons
label_style = {"font": ("Arial", 16, "bold"), "fg": "black", "bg": "white"}  # Change label color to black and background color to white
button_style = {"font": ("Arial", 12), "fg": "white", "bg": "#0074D9"}  # Change button color to blue

# Define the labels and buttons
temp_humid_label = tk.Label(root, text="DogHouse Temperature & Humidity", **label_style)
temp_humid_label.pack(pady=10)
temp_humid_button = tk.Button(root, text="Check", command=lambda: print("Currently DogHouse Temperature & Humidity"), **button_style)
temp_humid_button.pack()

water_temp_label = tk.Label(root, text="Water Temperature", **label_style)
water_temp_label.pack(pady=10)
water_temp_button = tk.Button(root, text="Check", command=lambda: print("Currently Water Temperature"), **button_style)
water_temp_button.pack()

food_weight_label = tk.Label(root, text="Food Weight", **label_style)
food_weight_label.pack(pady=10)
food_weight_button = tk.Button(root, text="Check", command=lambda: print("Food Weight"), **button_style)
food_weight_button.pack()



dog_weight_label = tk.Label(root, text="Dog Weight", **label_style)
dog_weight_label.pack(pady=10)
dog_weight_button = tk.Button(root, text="Check", command=lambda: print("Dog Weight"), **button_style)
dog_weight_button.pack()



plot_label = tk.Label(root, text="Graphs", **label_style)
plot_label.pack(pady=10)



weight_graph_button = tk.Button(root, text="Weight Graph", command=lambda: print("Weight Graph"), **button_style)
weight_graph_button.pack(side='left', padx=5, pady=5)

temp_graph_button = tk.Button(root, text="Temperature Graph", command=lambda: print("Temperature Graph"), **button_style)
temp_graph_button.pack(side='left', padx=5, pady=5)

water_graph_button = tk.Button(root, text="Water Consuming Graph", command=lambda: print("I LOVE TO DRINK"), **button_style)
water_graph_button.pack(side='left', padx=5, pady=5)

food_graph_button = tk.Button(root, text="Food Consuming Graph", command=lambda: print("I LOVE TO EAT"), **button_style)
food_graph_button.pack(side='left', padx=5, pady=5)

# Define the plot window for the graphs
fig = Figure(figsize=(6, 4), dpi=100)
plot_window = FigureCanvasTkAgg(fig, root)
plot_window.get_tk_widget().pack(padx=20, pady=10, side=tk.BOTTOM, fill=tk.BOTH, expand=1)

root.mainloop()