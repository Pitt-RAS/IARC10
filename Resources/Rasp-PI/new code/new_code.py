import cv2 as cv
import numpy as np
from picamera2 import Picamera2
import time

# Load the pre-trained model for object detection
net = cv.dnn.readNetFromCaffe('/home/ras-1212/Documents/IARC10/Resources/Rasp-PI/new code/MobileNetSSD_deploy.prototxt', '/home/ras-1212/Documents/IARC10/Resources/Rasp-PI/new code/MobileNetSSD_deploy.caffemodel')

# Initialize the camera
picam2 = Picamera2()
picam2.start_preview()
time.sleep(2)  # Allow time for the camera to adjust

# Load class labels
with open('/home/ras-1212/Documents/IARC10/Resources/Rasp-PI/new code/coco_labels.txt', 'r') as f:
    class_labels = f.read().splitlines()

while True:
    # Capture a frame from the camera
    frame = picam2.capture_array()

    # Perform object detection
    blob = cv.dnn.blobFromImage(cv.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    # Loop over the detections and draw bounding boxes around detected objects
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            (startX, startY, endX, endY) = box.astype("int")
            cv.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

            # Get the class ID and accuracy for the current detection
            class_id = int(detections[0, 0, i, 1])
            accuracy = detections[0, 0, i, 2]

            # Get the class name corresponding to the class ID
            class_name = class_labels[class_id-15]

            # Draw the class name and accuracy on top of the bounding box
            label = f'{class_name}: {round(accuracy * 100, 2)}%'
            cv.putText(frame, label, (startX, startY - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the resulting frame
    cv.imshow('Object Detection', frame)

    # Break the loop if 'q' is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
picam2.stop_preview()
cv.destroyAllWindows()
