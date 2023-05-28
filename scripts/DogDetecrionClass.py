import cv2
import numpy as np
import json
from tensorflow.keras.models import load_model
from comvert2tflite import load_tflite_model


class ObjectDetection:
    def __init__(self, weights_path="../dnn_model/yolov4-tiny.weights",
                 cfg_path="../dnn_model/yolov4-tiny.cfg",
                 breed_model_path="../dnn_model/breed/dog_breed_model.h5",
                 pose_model_path="../dnn_model/pose/pose_model.h5"):
        print("Loading Object Detection")
        self.nmsThreshold = 0.6
        self.confThreshold = 0.6
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
        self.model.setInputParams(size=self.image_size, scale=1 / 255)

        print("Loading Dog breed recognition net (tf)")
        self.breed_model = load_model(breed_model_path)

        print("Loading Dog pose recognition net (tf)")
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
        breed_prediction_label = [key for key, value in self.breed_classes.items() if
                                  value == breed_prediction.argmax()]
        return breed_prediction_label[0], breed_prediction.max() * 100

    def pose_detect(self, frame):
        resized = cv2.resize(frame, self.pose_image_size, interpolation=cv2.INTER_AREA)
        img = np.array(resized)
        img = img / 255.0
        # Object Detection
        pose_prediction = self.pose_model.predict(img[None, :, :])
        pose_prediction_label = [key for key, value in self.pose_classes.items() if value == pose_prediction.argmax()]
        return pose_prediction_label[0], pose_prediction.max() * 100

    def detect(self, frame):
        return self.model.detect(frame, nmsThreshold=self.nmsThreshold, confThreshold=self.confThreshold)


class TfliteObjectDetection:
    def __init__(self, weights_path="../dnn_model/yolov4-tiny.weights",
                 cfg_path="../dnn_model/yolov4-tiny.cfg",
                 breed_model_path="../dnn_model/breed/dog_breed_model.tflite",
                 pose_model_path="../dnn_model/pose/pose_model.tflite"):

        print("Loading Object Detection")
        self.nmsThreshold = 0.4
        self.confThreshold = 0.5
        self.image_size = (320, 320)

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
        self.model.setInputParams(size=self.image_size, scale=1 / 255)

        print("Loading Dog breed recognition net (tflite)")
        self.breed_model = load_tflite_model(breed_model_path)
        self.breed_image_size = self.breed_model.get_input_details()[0]['shape'][1:3]

        print("Loading Dog pose recognition net (tflite)")
        self.pose_model = load_tflite_model(pose_model_path)
        self.pose_image_size = self.pose_model.get_input_details()[0]['shape'][1:3]

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

    def preprocess_image(self, image, input_shape):
        image = cv2.resize(image, input_shape, interpolation=cv2.INTER_AREA)
        image_array = np.array(image) / 255.0
        image_array = image_array.astype(np.float32)  # Cast the image array to float32
        return np.expand_dims(image_array, axis=0)

    def predict(self, interpreter, input_image):
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        interpreter.set_tensor(input_details[0]['index'], input_image)
        interpreter.invoke()

        return interpreter.get_tensor(output_details[0]['index'])

    def lite_predict(self, image, mode):
        if mode == "breed":
            interpreter = self.breed_model
            classes = self.breed_classes
            input_shape = self.breed_image_size
        else:
            interpreter = self.pose_model
            classes = self.breed_classes
            input_shape = self.pose_image_size
        # Preprocess the image
        input_image = self.preprocess_image(image, input_shape)
        # Predict the image
        prediction = self.predict(interpreter, input_image)
        # Process the results and display the predicted class
        predicted_class = np.argmax(prediction)
        prediction_label = [key for key, value in classes.items() if value == np.argmax(predicted_class)]

        # print("Predicted class:", prediction_label[0], " with:", np.max(prediction))
        return prediction_label[0], np.max(prediction) * 100

    def detect(self, frame):
        return self.model.detect(frame, nmsThreshold=self.nmsThreshold, confThreshold=self.confThreshold)
