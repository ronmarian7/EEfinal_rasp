import cv2
from tensorflow.keras.models import load_model
import numpy as np
import json

# Load the Keras model
pose_model = load_model('../dnn_model/pose/pose_model.h5')
with open("../dnn_model/pose/class.json","r") as f:
    class_indices = json.load(f)

def predict_pose(frame):
    resized = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
    img = np.array(resized)
    img = img / 255.0
    # Object Detection
    pose_prediction = pose_model.predict(img[None, :, :])
    pose_prediction_label = [key for key, value in class_indices.items() if value == pose_prediction.argmax()]
    # return the pose_prediction
    return pose_prediction_label[0], pose_prediction.max()*100

if __name__ == '__main__':
    img = cv2.imread('../Picture/dog sitting_6.jpg')
    print(predict_pose(img))