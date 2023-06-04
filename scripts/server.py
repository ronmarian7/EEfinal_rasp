#!/usr/bin/env python3
import socket
from time import sleep
import random
from datetime import datetime
from food_weight import *
from feeder import *
from humidity_tmp import *
from water_temp import *
from water_weight import *
from doghouse_weight import * 

"""
TODOs 
1. change to the actual data from the sensors
"""


def get_sensor_data(doghouse_weight_m, hx1, hx2, humidity_tmp_m,water_weight_m, config_weight):
    """
    Getting the data from the sensors
    Currently the data that is generated is random
    :return: The data from the sensors in a string containing the format of commas
    """
  
    area_temperature, area_humidity = get_humidity_tmp(humidity_tmp_m)

    dog_weight = get_doghouse_weight(doghouse_weight_m)

    food_weight, config_weight = handle_feeder(hx1, hx2, portions=10, feedingthreshold=50)

    water_weight = get_water_weight(water_weight_m)

    water_temperature = get_water_temp()

    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("Time - {}  area_temperature: {:.1f} C    area_humidity: {}%  dog_weight: {}KG    food_weight: {}gr\
       water_weight: {}ml    water_temperature: {}C".format(time, area_temperature, area_humidity, dog_weight,
                                                            food_weight, water_weight, water_temperature))
    data = f'{time},{area_temperature},{area_humidity},{dog_weight},{food_weight},{water_weight},{water_temperature}'
    return data, config_weight


def socket_server(HOST, PORT=65432, x=10):
    """
    Setting the server socket and waiting for a client to connect
    After connecting, sends the data every x seconds
    :param HOST:
    :param PORT:
    :param x: The time interval between sending data
    :return:
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Server Started waiting for client to connect in IP: {HOST}, PORT: {PORT} ")
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)
            doghouse_weight_m = config_doghouse_weight()
            hx1, hx2, config_weight = config_feeder()
            humidity_tmp_m = config_humidity_tmp()
            water_weight_m = config_water_weight()
            while True:
                print("Sending data ")
                my_data, config_weight = get_sensor_data(doghouse_weight_m, hx1, hx2, humidity_tmp_m, water_weight_m, config_weight)
                x_encoded_data = my_data.encode('utf-8')
                conn.sendall(x_encoded_data)
                sleep(x)


if __name__ == '__main__':
    HOST = socket.gethostbyname(socket.gethostname())
    try:
        socket_server(HOST="192.168.158.4")
    except (ConnectionResetError, KeyboardInterrupt, ConnectionAbortedError):
        print("The connection was aborted by the client")
    except Exception as e:
        raise e
