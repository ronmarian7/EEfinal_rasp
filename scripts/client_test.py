import time
import struct
import datetime
import socket



HOST = '192.168.1.129'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
received_data = []


def client_socket():

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		while True:
			command = input('Enter command: ')
			if command == 'quit':
				break
			s.sendall(command.encode())

			# Receive data from the socket connection
			data = s.recv(1024).decode()
			temperature, humidity = data.split(',')

			print("Temperature {}".format(temperature))
			print("Humidity {}".format(humidity))

			time.sleep(5)


if __name__ == "__main__":
	client_socket()
