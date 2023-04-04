import cv2
import numpy as np
import json
from tensorflow.keras.models import load_model


class ObjectDetection:
    def __init__(self, weights_path="../dnn_model/yolov4-tiny.weights",
                 cfg_path="../dnn_model/yolov4-tiny.cfg",
                 breed_model_path="../dnn_model/breed/dog_breed_model.h5",
                 pose_model_path="../dnn_model/pose/pose_model.h5"):
        print("Loading Object Detection")
        self.nmsThreshold = 0.4
        self.confThreshold = 0.5
        self.image_size = (320, 320)

        self.breed_image_size = (299, 299)
        self.pose_image_size = (224, 224)

        self.classes = []
        self.breed_classes = {}
        self.pose_classes = {}

        self.load_class()
        self.load_breed_class()
        self.load_pose_class()

        # Load Network
        print("Loading Dog recognition net")
        dog_net = cv2.dnn.readNet(weights_path, cfg_path)
        self.model = cv2.dnn_DetectionModel(dog_net)
        self.model.setInputParams(size=self.image_size, scale=1/255)

        print("Loading Dog breed recognition net")
        self.breed_model = load_model(breed_model_path)

        print("Loading Dog pose recognition net")
        self.pose_model = load_model(pose_model_path)

    def load_class(self, classes_path="../dnn_model/classes.txt"):
        with open(classes_path, "r") as file_object:
            for class_name in file_object.readlines():
                class_name = class_name.strip()
                self.classes.append(class_name)
        return self.classes

    def load_breed_class(self, classes_path="../dnn_model/breed/class.json"):
        with open(classes_path, "r") as f:
            self.breed_classes = json.load(f)
        return self.breed_classes

    def load_pose_class(self, classes_path="../dnn_model/pose/class.json"):
        with open(classes_path, "r") as f:
            self.pose_classes = json.load(f)
        return self.pose_classes

    def breed_detect(self, frame):
        resized = cv2.resize(frame, self.breed_image_size, interpolation=cv2.INTER_AREA)
        img = np.array(resized)
        img = img / 255.0
        # Object Detection
        breed_prediction = self.breed_model.predict(img[None, :, :])
        breed_prediction_label = [key for key, value in self.breed_classes.items() if value == breed_prediction.argmax()]
        return breed_prediction_label[0], breed_prediction.max()*100

    def pose_detect(self, frame):
        resized = cv2.resize(frame, self.pose_image_size, interpolation=cv2.INTER_AREA)
        img = np.array(resized)
        img = img / 255.0
        # Object Detection
        pose_prediction = self.pose_model.predict(img[None, :, :])
        pose_prediction_label = [key for key, value in self.pose_classes.items() if value == pose_prediction.argmax()]
        return pose_prediction_label[0], pose_prediction.max()*100

    def detect(self, frame):
        return self.model.detect(frame, nmsThreshold=self.nmsThreshold, confThreshold=self.confThreshold)
