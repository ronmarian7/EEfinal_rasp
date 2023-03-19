import struct
import datetime
import socket
import json
import os


HOST = '192.168.1.129'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

area_temperature = {}
area_humidity = {}
dog_weight = {}
food_weight = {}
water_weight = {}
water_temperature = {}

def load_data():
	global area_temperature, area_humidity
	# if this file exists then we can assume that all the other files exists
	if os.path.exists(r"..\\data\\area_temperature.json"):
		with open(r"..\\data\\area_temperature.json", "r") as f:
			area_temperature = json.load(f)
		with open(r"..\\data\\area_humidity.json", "a") as f:
			area_humidity = json.load(f)
		# with open(r"../data/dog_weight.json", "a") as f:
		# 	dog_weight = json.load(f)
		# with open(r"../data/food_weight.json", "a") as f:
		# 	food_weight = json.load(f)
		# with open(r"../data/water_weight.json", "a") as f:
		# 	water_weight = json.load(f)
		# with open(r"../data/water_temperature.json", "a") as f:
		# 	water_temperature = json.load(f)

def dump_data():
	with open(r"../data/area_temperature.json", "a") as f:
		json.dump(area_temperature, f)
	with open(r"../data/area_humidity.json", "a") as f:
		json.dump(area_humidity, f)
	# with open(r"../data/dog_weight.json", "a") as f:
	# 	json.dump(dog_weight, f)
	# with open(r"../data/food_weight.json", "a") as f:
	# 	json.dump(food_weight, f)
	# with open(r"../data/water_weight.json", "a") as f:
	# 	json.dump(water_weight, f)
	# with open(r"../data/water_temperature.json", "a") as f:
	# 	json.dump(water_temperature, f)



def client_socket():
	load_data() # load the history of the data

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		while True:
			# Receive data from the socket connection
			data = s.recv(1024).decode()
			# process the data to variables
			time, temperature, humidity = data.split(',')

			print(f"Time {time}")
			print(f"Temperature {temperature}")
			area_temperature[time] = temperature
			print(f"Humidity {humidity}")
			area_humidity[time] = humidity




if __name__ == "__main__":
	try:
		client_socket()
	except Exception as e:
		raise e
	finally:
		dump_data()