#!/usr/bin/env python3

import socket
import numpy as np
import encodings
import board
import adafruit_dht
import time



HOST = '192.168.231.4'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


dhtDevice = adafruit_dht.DHT22(board.D17, use_pulseio=False)

def random_data():
    temperature_f = 20
    temperature_c = 50
    humidity = 80
    print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))
    data = '{},{}'.format(temperature_c,humidity)

    return data
 

 

def my_server():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Server Started waiting for client to connect ")
        s.bind((HOST, PORT))
        s.listen(5)
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)
            while True:

                data = conn.recv(1024).decode('utf-8')

                if str(data) == "Data":

                    print("Ok Sending data ")

                    my_data = random_data()

                    x_encoded_data = my_data.encode('utf-8')

                    conn.sendall(x_encoded_data)

                elif  str(data) == "Quit":
                    print("shutting down server ")
                    break

                # if not data:
                #   break
                else:
                    pass


if __name__ == '__main__':
    while 1:
        my_server()