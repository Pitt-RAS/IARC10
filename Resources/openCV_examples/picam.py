from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import math
from ultralytics import YOLO

# initialize PiCamera
camera = PiCamera()
camera.resolution(640, 480)
camera.framerate = 32
raw = PiRGBArray(camera, size=(640, 480))

# give camera time to warmup
time.sleep(0.1)

# model trained from https://cocodataset.org/#home which is just a whole bunch of common objects
model = YOLO("yolo-Weights/yolov8n.pt")

# diff possible objects (NOTE: this part wont be needed if we train our own model)
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

# this is the point from which we will get the depth
def midpoint(ptA, ptB):
    return int((ptA[0] + ptB[0]) * 0.5), int((ptA[1] + ptB[1]) * 0.5)


# capture frames
for frame in camera.capture_continuous(raw, format='bgr', use_video_port=True):
    image = frame.array

    results = model(image, stream=True)

    for r in results:
        #yolo returns the coords of a bounding box around the object
        boxes = r.boxes

        for box in boxes:
            # define boxes around each detected object and draw a rectangle
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence of object
            confidence = math.ceil((box.conf[0]*100))/100
            #print("Confidence = ",confidence)

            # object type
            cls = int(box.cls[0])
            #print("Object: ", classNames[cls])

            # printing details of object on frame
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2


            #cv2.putText(color_image, classNames[cls], org, font, fontScale, color, thickness)
            cv2.putText(image, str(round(dist,2)), org, font, fontScale, color, thickness)

    # show image
    cv2.imshow("color", image)
    
    # clear stream to prep for next image
    raw.truncate(0)

    # break
    if cv2.waitKey(1) == ord('q'):
        break

    
