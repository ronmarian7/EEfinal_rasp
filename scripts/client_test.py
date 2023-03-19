import struct
import datetime
import socket
import json
import os


HOST = '192.168.1.129'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

area_temperature_d = {}
area_humidity_d = {}
dog_weight_d = {}
food_weight_d = {}
water_weight_d = {}
water_temperature_d = {}

def load_data():
	global area_temperature_d, area_humidity_d, dog_weight_d, food_weight_d, water_weight_d, water_temperature_d
	# if this file exists then we can assume that all the other files exists
	if os.path.exists("data\\area_temperature.json"):
		with open("data\\area_temperature.json", "r") as f:
			area_temperature_d = json.load(f)
		with open("data\\area_humidity.json", "a") as f:
			area_humidity_d = json.load(f)
		with open("\\data\\dog_weight.json", "a") as f:
			dog_weight_d = json.load(f)
		with open("data\\food_weight.json", "a") as f:
			food_weight_d = json.load(f)
		with open("data\\water_weight.json", "a") as f:
			water_weight_d = json.load(f)
		with open("data\\water_temperature.json", "a") as f:
			water_temperature_d = json.load(f)

def dump_data():
	with open("data\\area_temperature.json", "a") as f:
		json.dump(area_temperature_d, f)
	with open("data\\area_humidity.json", "a") as f:
		json.dump(area_humidity_d, f)
	with open("data\\dog_weight.json", "a") as f:
		json.dump(dog_weight_d, f)
	with open("data\\food_weight.json", "a") as f:
		json.dump(food_weight_d, f)
	with open("data\\water_weight.json", "a") as f:
		json.dump(water_weight_d, f)
	with open("data\\water_temperature.json", "a") as f:
		json.dump(water_temperature_d, f)


def client_socket():
	global area_temperature_d, area_humidity_d, dog_weight_d, food_weight_d, water_weight_d, water_temperature_d
	load_data() # load the history of the data if available

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		while True:
			# Receive data from the socket connection
			data = s.recv(1024).decode()
			# Check if there are 6 commas (and 7 elements) before splitting the string
			assert data.count(",") == 6, "Error: Data string does not have the expected number of elements."
			# process the data to variables
			time, area_temperature, area_humidity, dog_weight, food_weight, water_weight, water_temperature = data.split(',')

			print(f"Time {time}")
			print(f"Area_temperature {area_temperature}")
			area_temperature_d[time] = area_temperature

			print(f"Area_humidity {area_humidity}")
			area_humidity_d[time] = area_humidity

			print(f"Dog_weight {dog_weight}")
			dog_weight_d[time] = dog_weight

			print(f"Food_weight {food_weight_d}")
			food_weight_d[time] = food_weight

			print(f"Area_humidity {water_weight}")
			water_weight_d[time] = water_weight

			print(f"Area_humidity {water_temperature}")
			water_temperature_d[time] = water_temperature


if __name__ == "__main__":
	try:
		client_socket()
	except Exception as e:
		raise e
	finally:
		dump_data()