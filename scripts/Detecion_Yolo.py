from ultralytics import YOLO
from DogDetecrionClass import PoseDetection
import cv2
import json
import math

breed_model = YOLO("../runs/detect/train15/weights/best.pt")
pose_model = YOLO("../runs/classify/train15/weights/best.pt")
ob = PoseDetection()

with open("../dnn_model/breed/class.json", "r") as f:
    breed_names = json.load(f)
pose_names = {0: 'Lying', 1: 'Sitting', 2: 'Standing'}

# video_path = "../videos/dell vid/dell1.mp4"  # false rec standing, but after is correct, Good breed detection
# video_path = "../videos/dell vid/dell2.mp4"  # Bad video, not to use
# video_path = "../videos/dell vid/dell3.mp4"  # Bad video, not to use
# video_path = "../videos/dell vid/dell4.mp4"  # Not detecting well
# video_path = "../videos/dell vid/dell5.mp4"  # Bad breed detection, Good pose detection
# video_path = "../videos/white_dog.mp4"
video_path = "../videos/beber.mp4"

cap = cv2.VideoCapture(video_path)
WindowName = "Webcam"
color = (255, 0, 0)
font = cv2.FONT_HERSHEY_COMPLEX
FONT_SCALE = 1e-3  # Adjust for larger font size in all images
THICKNESS_SCALE = 1e-3  # Adjust for larger thickness in all images
roi_space = 100
conf = 0.55
fps = cap.get(cv2.CAP_PROP_FPS)
cv2.namedWindow(WindowName, cv2.WINDOW_NORMAL)
# cv2.resizeWindow(WindowName, 1280, 720)
# cv2.resizeWindow(WindowName, 848, 480)

# These two lines will force "Main View" window to be on top with focus.
cv2.setWindowProperty(WindowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setWindowProperty(WindowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)

try:
    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Run YOLOv8 inference on the frame
            breed_results = breed_model.predict(frame, conf=conf)
            height, width, _ = frame.shape
            font_scale = min(width, height) * FONT_SCALE
            thickness = math.ceil(min(width, height) * THICKNESS_SCALE)

            # Object Detection
            breed_boxes = [box.xyxy.to('cpu').tolist() for box in breed_results[0].boxes]
            breed_class_ids = breed_results[0].boxes.cls.to('cpu').tolist()
            breed_scores = breed_results[0].boxes.conf.to('cpu').tolist()
            for breed_classId, breed_score, box in zip(breed_class_ids, breed_scores, breed_boxes):
                box = box[0]
                x, y, w, h = list(map(int, box))
                breed_name = [key for key, value in breed_names.items() if value == breed_classId][0]
                cv2.rectangle(frame, (x, y), (w, h), color, 2)
                cv2.putText(frame, f"Breed: {breed_name} - {breed_score:.3f}", (int(box[0]), int(box[1] - 35)),
                            font, font_scale, color, thickness)
                roi = frame[max(0, y - roi_space):min(height, h + roi_space), max(0, x - roi_space):min(width, w + roi_space)]
                pose_label, pose_label_score = ob.pose_detect(roi)
                # Add the text to the image
                cv2.putText(frame, f'Pose: {pose_label} - {pose_label_score:.3f}', (int(box[0]), int(box[1] - 5)), font,
                            font_scale, color, thickness)

            cv2.imshow("Webcam", frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Break the loop if the end of the video is reached
            break
except Exception as e:
    raise e
finally:
    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()
