#! /usr/bin/python3

from PinConfig import *
from doghouse_weight import *
from food_weight import *
from humidity_tmp import *
from water_temp import *
from water_weight import *

if __name__ == '__main__':
    doghouse_weight_m = config_doghouse_weight(dtpin=DOGHOUSE_WEIGHT_DTPIN, sckpin=DOGHOUSE_WEIGHT_SCKPIN,
                                               referenceUnit=DOGHOUSE_REFERENCE_UNIT)
    hx1, hx2, config_weight = config_feeder(dtpin1=FOOD_WEIGHT_DTPIN1, sckpin1=FOOD_WEIGHT_SCKPIN1,
                                            dtpin2=FOOD_WEIGHT_DTPIN2, sckpin2=FOOD_WEIGHT_SCKPIN2,
                                            config_range=FOOD_WEIGHT_CONFIG_RANGE,
                                            referenceUnit=FOOD_WEIGHT_REFERENCE_UNIT)
    humidity_tmp_m = config_humidity_tmp(pin=HUM_TEMP_PIN)
    water_weight_m = config_water_weight(dtpin=WATER_WEIGHT_DTPIN, sckpin=WATER_WEIGHT_SCKPIN,
                                         referenceUnit=WATER_WEIGHT_REFERENCE_UNIT)

    while True:
        print("---------------------------------------------")
        doghouse_weight = get_doghouse_weight(doghouse_weight_m)
        temperature_c, humidity = get_humidity_tmp(humidity_tmp_m, referenceUnit=HUM_TEMP_REFERENCE_UNIT)
        water_temp = get_water_temp()
        food_weight, config_weight = handle_feeder(hx1, hx2, cur_ref_weight=config_weight, portions=FEEDER_PORTIONS,
                                                   feedingthreshold=FEEDER_THRESHOLD, feederpin=FEEDER_PIN)
        water_weight = get_water_weight(water_weight_m)
        print("---------------------------------------------")
