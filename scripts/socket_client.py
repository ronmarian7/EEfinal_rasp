import socket
import time
import struct
import datetime


def client_socket():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server
    # Define the format string for the struct
    struct_format = '3i 3f Q'
    sensor_data = struct.Struct(struct_format)

    received_data = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
        socket.connect((HOST, PORT))

        while True:
            command = input(
                'Enter command (get_all, get_weight, get_temperature, get_humidity, quit): ')
            if command == 'quit':
                break
            client_socket.sendall(command.encode())

            # Receive data from the socket connection
            data = client_socket.recv(1024)

            # Unpack the received data into an array of tuples
            while data:
                reading = sensor_data.unpack(data[:sensor_data.size])
                received_data.append(reading)
                data = data[sensor_data.size:]

            # TODO for all the data
            y_humidity = received_data[0][0]
            x_temperature = received_data[0][1]

            print("Temperature {}".format(x_temperature))
            print("Humidity {}".format(y_humidity))

            time.sleep(5)


if __name__ == "__main__":
    client_socket()
