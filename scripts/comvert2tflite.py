import tensorflow as tf
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

def convert2tflite(model_name):
    # Load the H5 model
    h5_model = tf.keras.models.load_model(f"{model_name}.h5")
    # Convert the model to TFLite format
    converter = tf.lite.TFLiteConverter.from_keras_model(h5_model)
    converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_LATENCY]
    tflite_model = converter.convert()
    # Save the TFLite model to a file
    with open(f"{model_name}.tflite", 'wb') as f:
        f.write(tflite_model)


def preprocess_ext_image(image_path, input_shape):
    image = Image.open(image_path).convert('RGB')
    image = image.resize(input_shape, Image.LANCZOS)  # Use LANCZOS instead of deprecated ANTIALIAS
    image_array = np.array(image) / 255.0
    image_array = image_array.astype(np.float32)  # Cast the image array to float32
    return np.expand_dims(image_array, axis=0)

def preprocess_image(image, input_shape):
    image = image.resize(input_shape, Image.LANCZOS)  # Use LANCZOS instead of deprecated ANTIALIAS
    image_array = np.array(image) / 255.0
    image_array = image_array.astype(np.float32)  # Cast the image array to float32
    return np.expand_dims(image_array, axis=0)

def load_tflite_model(model_path):
    with open(model_path, 'rb') as f:
        model_content = f.read()

    interpreter = tf.lite.Interpreter(model_content=model_content)
    interpreter.allocate_tensors()
    return interpreter


def predict_image(interpreter, input_image):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], input_image)
    interpreter.invoke()

    return interpreter.get_tensor(output_details[0]['index'])


def lite_predict_img(image_path, tflite_model_path):
    # Get the input shape of the TFLite model
    interpreter = load_tflite_model(tflite_model_path)
    input_shape = interpreter.get_input_details()[0]['shape'][1:3]
    # Preprocess the image
    input_image = preprocess_ext_image(image_path, input_shape)
    # Predict the image
    prediction = predict_image(interpreter, input_image)
    # Process the results and display the predicted class
    predicted_class = np.argmax(prediction)
    print("Predicted class:", predicted_class, " with:", np.max(prediction))

def full_predict_img(image_path, tf_model_path):
    h5_model = load_model(tf_model_path)
    # Get the input shape of the H5 model
    input_shape = h5_model.layers[0].input_shape[0][1:3]
    # Preprocess the image
    input_image = preprocess_ext_image(image_path, input_shape)
    # Predict the image
    prediction = h5_model.predict(input_image)
    # Process the results and display the predicted class
    predicted_class = np.argmax(prediction)
    print("Predicted class:", predicted_class, " with:", np.max(prediction))

if __name__ == '__main__':
    image_path = "../Picture/English_setter.jpeg"
    tf_model_path = "../dnn_model/pose/pose_model.h5"
    tflite_model_path = "../dnn_model/pose/pose_model.tflite"
    print("FULL")
    full_predict_img(image_path, tf_model_path)
    print("LITE")
    lite_predict_img(image_path, tflite_model_path)
    # convert2tflite("../dnn_model/breed/dog_breed_model")