#!/usr/bin/env python3
import socket
from datetime import datetime
from time import sleep

from PinConfig import *
from doghouse_weight import *
from food_weight import *
from humidity_tmp import *
from water_temp import *
from water_weight import *

"""
TODOs 
1. change to the actual data from the sensors
"""


def get_sensor_data(doghouse_weight_m, feeder_1_m, feeder_2_m, humidity_tmp_m, water_weight_m, config_weight):
    """
    Getting the data from the sensors
    Currently the data that is generated is random
    :return: The data from the sensors in a string containing the format of commas
    """

    dog_weight = get_doghouse_weight(doghouse_weight_m)
    food_weight, config_weight = handle_feeder(feeder_1_m, feeder_2_m, cur_ref_weight=config_weight,
                                               portions=FEEDER_PORTIONS,
                                               feedingthreshold=FEEDER_THRESHOLD, feederpin=FEEDER_PIN)
    water_weight = get_water_weight(water_weight_m)
    water_temperature = get_water_temp()
    area_temperature, area_humidity = get_humidity_tmp(humidity_tmp_m, referenceUnit=HUM_TEMP_REFERENCE_UNIT)

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
            # CONFIGURING THE SENSORS
            doghouse_weight_m = config_doghouse_weight(dtpin=DOGHOUSE_WEIGHT_DTPIN, sckpin=DOGHOUSE_WEIGHT_SCKPIN,
                                                       referenceUnit=DOGHOUSE_REFERENCE_UNIT)
            feeder_1_m, feeder_2_m, config_weight = config_feeder(dtpin1=FOOD_WEIGHT_DTPIN1,
                                                                  sckpin1=FOOD_WEIGHT_SCKPIN1,
                                                                  dtpin2=FOOD_WEIGHT_DTPIN2,
                                                                  sckpin2=FOOD_WEIGHT_SCKPIN2,
                                                                  config_range=FOOD_WEIGHT_CONFIG_RANGE,
                                                                  referenceUnit=FOOD_WEIGHT_REFERENCE_UNIT)
            humidity_tmp_m = config_humidity_tmp(pin=HUM_TEMP_PIN)
            water_weight_m = config_water_weight(dtpin=WATER_WEIGHT_DTPIN, sckpin=WATER_WEIGHT_SCKPIN,
                                                 referenceUnit=WATER_WEIGHT_REFERENCE_UNIT)
            while True:
                print("Sending data ")
                my_data, config_weight = get_sensor_data(doghouse_weight_m, feeder_1_m, feeder_2_m, humidity_tmp_m,
                                                         water_weight_m,
                                                         config_weight)
                x_encoded_data = my_data.encode('utf-8')
                conn.sendall(x_encoded_data)
                sleep(x)


if __name__ == '__main__':
    HOST = socket.gethostbyname(socket.gethostname())
    try:
        socket_server(HOST=HOST, PORT=HOST_PORT, x=HOST_ITER_DELTA_SEC)
    except (ConnectionResetError, KeyboardInterrupt, ConnectionAbortedError):
        print("The connection was aborted by the client")
    except Exception as e:
        raise e
