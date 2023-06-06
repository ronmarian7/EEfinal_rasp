#! /usr/bin/python3

from food_weight import *
from feeder import *
from humidity_tmp import *
from water_temp import *
from water_weight import *
from doghouse_weight import *
from time import sleep 


if __name__ == '__main__':
   doghouse_weight_m = config_doghouse_weight()
   hx1, hx2, config_weight = config_feeder()
   humidity_tmp_m = config_humidity_tmp()
   water_weight_m = config_water_weight()
   
   while True:
      print("---------------------------------------------")
      doghouse_weight = get_doghouse_weight(doghouse_weight_m)
      temperature_c, humidity = get_humidity_tmp(humidity_tmp_m)
      water_temp = get_water_temp()
      food_weight, config_weight = handle_feeder(hx1, hx2, cur_ref_weight=config_weight, portions=10, feedingthreshold=50)
      water_weight = get_water_weight(water_weight_m)
      print("---------------------------------------------")
      sleep(1)
