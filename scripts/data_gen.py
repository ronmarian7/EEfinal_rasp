import json
from datetime import datetime, timedelta
import random


def data_gen(file_name: str, l_lim=1, h_lim=50, days=7, samples=120):
    # Set the start time of the data generation to a week ago from today
    start_time = datetime.now() - timedelta(days=days)

    # Initialize an empty dictionary to store the data
    data = {}

    # Generate data samples
    for i in range(samples):
        # Add a new data sample with a timestamp and a random value
        timestamp_str = start_time.strftime("%d/%m/%Y %H:%M:%S")
        value = random.randint(l_lim, h_lim)
        data[timestamp_str] = value

        # Increment the timestamp by 10 seconds for the next sample
        start_time += timedelta(seconds=10)

    # Save the data to a JSON file
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile, indent=4)

if __name__ == '__main__':
    data_gen("../data/dog_food_consumption.json")
    data_gen("../data/dog_humidity.json")
    data_gen("../data/dog_temperatures.json")
    data_gen("../data/dog_water_consumption.json")
    data_gen("../data/dog_weights.json")
    data_gen("../data/water_temp.json")

