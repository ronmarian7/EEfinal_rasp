import cv2
from tensorflow.keras.models import load_model
import numpy as np
import json

# Load the Keras model
breed_model = load_model('../dnn_model/breed/dog_breed_model.h5')
with open("../dnn_model/breed/class.json","r") as f:
    class_indices = json.load(f)

def predict_breed(frame):
    resized = cv2.resize(frame, (299,299), interpolation=cv2.INTER_AREA)
    img = np.array(resized)
    img = img / 255.0
    # Object Detection
    breed_prediction = breed_model.predict(img[None, :, :])
    breed_prediction_label = [key for key, value in class_indices.items() if value == breed_prediction.argmax()]
    # return the breed_prediction
    return breed_prediction_label[0], breed_prediction.max()*100
