import cv2

# Opencv DNN
net = cv2.dnn.readNet("../dnn_model/yolov4-tiny.weights", "../dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320, 320), scale=1/255)


# Load class lists
classes = []
with open("../dnn_model/classes.txt", "r") as file_object:
    for class_name in file_object.readlines():
        class_name = class_name.strip()
        classes.append(class_name)

# Initialize a new cv2.VideoCapture object to capture video from the first camera
# cap = cv2.VideoCapture(2)
cap = cv2.VideoCapture("../videos/woman-play-with-corgi-dog.mp4")
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(3, 320)
cap.set(4, 320)
# FULL HD 1920 x 1080

# Create a named window with the desired size
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Frame", 320, 320)

wanted_classes = [16]  # 0  for person, 16 for dog

# Loop indefinitely to display video frames
while True:
    # Read a new frame from the video stream/
    ret, frame = cap.read()
    if not ret:
        break

    # Object Detection
    (class_ids, scores, boxes) = model.detect(frame, confThreshold=0.6, nmsThreshold=.4)
    for classId, score, box in zip(class_ids, scores, boxes):
        if classId in wanted_classes:
            (x, y, w, h) = box
            class_name = classes[classId]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{class_name.upper()} - {score:.3f}", (box[0] + 0, box[1] - 5),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)

    # Display the current frame
    cv2.imshow("Frame", frame)

    # Break the loop if the 'q' key is pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()