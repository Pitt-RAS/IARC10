import cv2 as cv
import numpy as np

# Load the pre-trained model for object detection
net = cv.dnn.readNetFromCaffe('/home/ras-1212/Documents/IARC10/Resources/Rasp-PI/new code/MobileNetSSD_deploy.prototxt', '/home/ras-1212/Documents/IARC10/Resources/Rasp-PI/new code/MobileNetSSD_deploy.caffemodel')

# Initialize the video capture object
cap = cv.VideoCapture(1)

while True:
    # Read frame from the webcam
    ret, frame = cap.read()

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
            # Get the class labels from coco_labels.txt
            with open('coco_labels.txt', 'r') as f:
                class_labels = f.read().splitlines()

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

# Release the video capture object and close all windows
cap.release()
cv.destroyAllWindows()