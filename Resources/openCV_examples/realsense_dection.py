from ultralytics import YOLO
import cv2
import pyrealsense2 as rs
import numpy as np
import math 


pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

profile = pipeline.start(config)

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

# main loop
while True:
    
    # get frame information
    frame = pipeline.wait_for_frames()
    color_frame = frame.get_color_frame()
    depth_frame = frame.get_depth_frame()
    # convert frames to numpy arrays (to make them usable for openCV)
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    

    #feeds camera image into the model, returns each detected object
    results = model(color_image, stream=True)

    for r in results:
        #yolo returns the coords of a bounding box around the object
        boxes = r.boxes

        for box in boxes:
            # define boxes around each detected object and draw a rectangle
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            cv2.rectangle(color_image, (x1, y1), (x2, y2), (255, 0, 255), 3)

            #get distance using depth frame
            midpoint_val = midpoint((x1,y1),(x2,y2))
            dist = depth_frame.get_distance(midpoint_val[0], midpoint_val[1])

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
            cv2.putText(color_image, str(round(dist,2)), org, font, fontScale, color, thickness)

    # show image
    cv2.imshow("color", color_image)

    # break
    if cv2.waitKey(1) == ord('q'):
        break
# terminate
pipeline.stop()
cv2.destroyAllWindows()




