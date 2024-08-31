# impot dependencies
from ultralytics import YOLO
import cv2
import pyrealsense2 as rs
import numpy as np
import math

# set up realsense pipeline
# we will be extracting depth, color, acceleration, and gyroscopic data
# would not recommend editing the parameters here
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.accel, rs.format.motion_xyz32f, 250)
config.enable_stream(rs.stream.gyro, rs.format.motion_xyz32f, 200)

# allows us to get acceleration and gyroscope data in a way that is easier to interpret
def get_accel_data(accel):
    return np.asanyarray([accel.x, accel.y, accel.z])

def get_gyro_data(gyro):
    return np.asanyarray([gyro.x, gyro.y, gyro.z])


profile = pipeline.start(config)

# choose the YOLO model - for deployment on a jetson you are either going to want the nano (yolov8n) or
# the small (yoloyv8s) YOLO weights
model = YOLO("yolo-Weights/yolov8n.pt")

# full list of classes of the COCO dataset that the base YOLO model is trained on
yolo_classes = [
              "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
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

# extract the midpoint
# this will be used to find the midpoint of the bounding boxes that the YOLO model
# spits out
# the midpoint will be where we extract object depth
def midpoint(point_a, point_b):
    return int((point_a[0] + point_b[0]) * 0.5), int((point_a[1] + point_b[1]) * 0.5)

# main loop
while True:

    # get frame information
    frame = pipeline.wait_for_frames()

    # print motion data
    # frame[2] and frame[3] are motion frames
    # as of right now I have no idea which one is the right one so I'm praying that I'm right
    accel = get_accel_data(frame[2].as_motion_frame().get_motion_data())
    gyro = get_gyro_data(frame[2].as_motion_frame().get_motion_data())
    print('accelerometer info', accel)
    print('gyroscope info', gyro)

    # get image and depth
    color_frame = frame.get_color_frame()
    depth_frame = frame.get_depth_frame()

    # convert color and depth frames into numpy arrays so that openCV can interpret them
    color_image = np.asanyarray(color_frame.get_data())
    depth_image = np.asanyarray(depth_frame.get_data())

    # get model detections
    results = model(color_image, stream = True)

    # draw bounding boxes
    for result in results:
        
        boxes = result.boxes

        for box in boxes:
            # get object class
            object_class = int(box.cls[0])

            # draw draw boxes and extract data if the class is "person"
            if object_class == 0:

                # get box coordinates and convert them to integers
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # draw the rectangle
                # params: image, top left, bottom right, box color (in BGR), line thickness
                cv2.rectangle(color_image, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # get distance using depth frame
                midpoint_value = midpoint((x1, y1), (x2, y2))
                distance = depth_frame.get_distance(midpoint_value[0], midpoint_value[1])

                # get object confidence
                # may be useful when testing models - but honestly you can
                # comment this out during final deployment
                confidence = math.ceil((box.conf[0] * 100)) / 100

                # printing details on box
                class_and_distance = yolo_classes[object_class] + str(round(distance, 2))
                origin = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                color = (255, 0, 0)
                thickness = 2

                cv2.putText(color_image, class_and_distance, origin, font, font_scale, color, thickness)

    # show the image
    cv2.imshow("color", color_image)

    # break the program gracefully
    if cv2.waitKey(1) == ord('q'):
        break

pipeline.stop()
cv2.destroyAllWindows()
