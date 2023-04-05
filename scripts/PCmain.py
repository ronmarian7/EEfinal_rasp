"""
Client
Manage to work in parallel
1. Receiving The data from the server
    a. Update the relevant csv every x sampling
    b. Save a variable of the latest sample value of every sensor
    c. Save a avg variable of all the samples so far
2. Running the GUI
    a. Sampling the data from  a variable of the latest sample value of a sensor when pressing a button
    b. Showing graphs of the sensor data by month/week/day by reading the data from a JSON file
    c. Detect anomalies in the data and alert if there are any


3. Running Image Processing
    a. Showing live on the screen the input from the webcam
    b. Show box of the dog
    c. On the Box show breed and pose with accuracy
"""

from DogDetection import image_processing

if __name__ == '__main__':
    image_processing()
