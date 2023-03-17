import threading
import socket
import struct
import time
import random
import datetime
import RPi.GPIO as GPIO

# define the struct format for sensor data
sensor_data_format = struct.Struct('2i 3f d')
# A condition object
condition = threading.Condition()

# function to collect sensor data
def collect_sensor_data(sensor_data):
   while True:
      # simulate reading sensor data
      humidity = random.randint(0, 100)
      temperature1 = random.uniform(0, 100)
      temperature2 = random.uniform(0, 100)
      weight1 = random.uniform(0, 1000)
      weight2 = random.uniform(0, 1000)
      weight3 = random.uniform(0, 1000)
      current_time = datetime.datetime.now()

      # pack sensor data into struct and add to the list
      packed_data = sensor_data_format.pack(humidity, temperature1, temperature2, weight1, weight2, weight3, current_time.timestamp())
      
      with condition: 
         sensor_data.append(packed_data)
         if len(sensor_data) > 31:
            condition.notify()

      time.sleep(1)

# function to send sensor data over socket
def send_sensor_data(client_socket, sensor_data):
   while True:
      # acquire mutex and get the next 32 entries of the list
      with condition:
         while len(sensor_data) < 32:
            condition.wait()

         data_to_send = sensor_data[:32]
         del sensor_data[:32]
   

      # pack data into a single bytes object
      data_bytes = b''.join(data_to_send)

      # send data over socket
      try:
         client_socket.sendall(data_bytes)
      except Exception as e:
         print(f"Error sending data: {e}")
         break
   # close the client socket
   client_socket.close()


# create a list to store sensor data # A shared resource
sensor_data = []

# create a thread to collect sensor data
collect_data_thread = threading.Thread(target=collect_sensor_data, args=(sensor_data,))
collect_data_thread.start()

# create a socket and listen for incoming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5000))
server_socket.listen()

# Accept a client connection
print("Waiting for client connection...")
client_socket, address = server_socket.accept()
print(f"Client connected from {address}")

# Create threads for data collection and socket connection
data_collection_thread = threading.Thread(target=collect_sensor_data, args=(sensor_data,))
socket_connection_thread = threading.Thread(target=send_sensor_data, args=(client_socket, sensor_data))

# Start both threads
data_collection_thread.start()
socket_connection_thread.start()

# Wait for threads to finish
socket_connection_thread.join()
# close the server socket
server_socket.close()
data_collection_thread.terminate()


# Clean up GPIO pins
GPIO.cleanup()

