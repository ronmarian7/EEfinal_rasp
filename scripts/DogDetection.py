import cv2
from DogDetecrionClass import ObjectDetection


def image_processing():
    ob = ObjectDetection()

    # Initialize a new cv2.VideoCapture object to capture video from the first camera
    # cap = cv2.VideoCapture(2)
    cap = cv2.VideoCapture("../videos/sitting_dog_vid.mp4")

    # Get the size of the video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # print("Video size:", width, "x", height)

    # Create a named window with the desired size
    cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Webcam", width//2, height//2)
    wanted_classes = [16]  # 0  for person, 16 for dog

    # Loop indefinitely to display video frames
    while True:
        # Read a new frame from the video stream/
        ret, frame = cap.read()
        if not ret:
            break

        # Object Detection
        (class_ids, scores, boxes) = ob.model.detect(frame)
        for classId, score, box in zip(class_ids, scores, boxes):
            if classId in wanted_classes:
                space = 50
                (x, y, w, h) = box
                roi = frame[y-space:y+h+space, x-space:x+w+space]
                class_name = ob.classes[classId]
                breed_label, breed_label_score = ob.breed_detect(roi)
                pose_label, pose_label_score = ob.pose_detect(roi)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"Breed: {breed_label} - {breed_label_score:.3f}", (box[0] + 0, box[1] - 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Pose: {pose_label} - {pose_label_score:.3f}", (box[0] + 0, box[1] - 5),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        # Display the current frame
        cv2.imshow("Webcam", frame)

        # Break the loop if the 'q' key is pressed
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # Release the VideoCapture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    image_processing()