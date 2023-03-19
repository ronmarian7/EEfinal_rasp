#!/usr/bin/env python3

import socket
import numpy as np
import encodings
from time import sleep
import random


HOST = '192.168.1.129'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


def random_data():
    temperature = random.randint(0, 100)
    humidity = random.randint(0, 100)
    print("Temp: {:.1f} C    Humidity: {}% ".format(temperature, humidity))
    data = '{},{}'.format(temperature, humidity)

    return data


def my_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Server Started waiting for client to connect ")
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)
            while True:
                print("Ok Sending data ")
                my_data = random_data()
                x_encoded_data = my_data.encode('utf-8')
                conn.sendall(x_encoded_data)
                sleep(1)


if __name__ == '__main__':
    my_server()