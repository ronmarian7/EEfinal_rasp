#!/usr/bin/env python3
import socket
from time import sleep
import random
from datetime import datetime

HOST = '192.168.1.129'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


def get_sensor_data():
    temperature = random.randint(0, 100)
    humidity = random.randint(0, 100)
    time = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    print("Time - {}  Temp: {:.1f} C    Humidity: {}% ".format(time, temperature, humidity))
    data = f'{time},{temperature},{humidity}'
    return data


def socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Server Started waiting for client to connect ")
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)
            while True:
                print("Sending data ")
                my_data = get_sensor_data()
                x_encoded_data = my_data.encode('utf-8')
                conn.sendall(x_encoded_data)
                sleep(1)


if __name__ == '__main__':
    socket_server()