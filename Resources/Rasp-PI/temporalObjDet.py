import cv2 as cv 
import numpy as np
from numpy import int16, uint8, log2

#Changeable variabels
camera = cv.VideoCapture(0)
ret, img_initial = camera.read()
resize_ratio = 1
pixel_thresh = 30
thresh = 0.5 #object detection threshold 
nms_threshold = 0.2 #0.1=no supress, 1=high supress 

#initial temp frame 
img_initial = cv.resize(img_initial,(1280//resize_ratio,720//resize_ratio))
img_initial = cv.flip(img_initial,1)
img_initial = cv.cvtColor(img_initial, cv.COLOR_BGR2GRAY)

#craete temp 2s array of pixels
temp_cont_frame = np.ones((img_initial.shape[0], img_initial.shape[1]))

classNames = []
classFile = 'C:/Users/Yun\Documents/Pitt RAS/Aerial/IARC10/Resources/Rasp-PI/coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

#get file paths
weightsPath = "C:/Users/Yun\Documents/Pitt RAS/Aerial/IARC10/Resources/Rasp-PI/frozen_inference_graph.pb"
configPath = "C:/Users/Yun\Documents/Pitt RAS/Aerial/IARC10/Resources/Rasp-PI/objectModel.pbtxt"

#network object setup
network = cv.dnn_DetectionModel(weightsPath,configPath)
network.setInputSize(320,320)
network.setInputScale(1.0/ 127.5)
network.setInputMean((127.5, 127.5, 127.5))
network.setInputSwapRB(True)

#pixel changer function
def change_pixels(image,image_initial):
    #iterate through a frame to compare each pixel of current frame to temp frame
    temp_cont_frame[...] = 0.5
    dif_frame = image.astype(int) - image_initial
    temp_cont_frame[dif_frame > pixel_thresh] = 1
    temp_cont_frame[dif_frame < -(pixel_thresh)] = 0
    return temp_cont_frame

#-----object detection function-----
def objectDetection(imgReg,ImgIrReg):#takes the convolved image, identifies objects, bounds objects with box and displays confidence of each prediction
    classIds, confidences, bbox = network.detect(imgReg,confThreshold=thresh)
    bbox = list(bbox)
    confidences = list(np.array(confidences).reshape(1,-1)[0])
    confidences = list(map(float,confidences))
    indices = cv.dnn.NMSBoxes(bbox,confidences,thresh,nms_threshold)
    if len(classIds) != 0:
        for i in indices:
            i = i[1]
            box = bbox[i]
            confidence = str(round(confidences[i]*100,2))
            x,y,w,h = box[0],box[1],box[2],box[3]
            cv.rectangle(ImgIrReg, (x,y), (x+w,y+h), color=(255,255,255), thickness=2)
            cv.putText(ImgIrReg, "Predicition: "+classNames[classIds[i][0]-1]+" "+confidence+"%",(x+10,y+20), cv.FONT_HERSHEY_PLAIN,1,color=(255,255,255),thickness=1)
    return ImgIrReg

#-----------------MAIN LOOP------------------
while True:
    #current frame object
    ret, img = camera.read()

    #current frame 
    img = cv.resize(img,(1280//resize_ratio,720//resize_ratio))
    img = cv.flip(img,1)
    imgCopy = img
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgTempContrasted = change_pixels(img, img_initial)
    #imgTemporalToBGR = cv.cvtColor(imgTempContrasted, cv.COLOR_GRAY2BGR)
    #call function to edit pixels
    cv.imshow("Video Feed", objectDetection(imgCopy,imgTempContrasted))
    #update temp frame to current frame
    img_initial = img
    
    if cv.waitKey(1) == ord("q"):
        break  
cv.destroyAllWindows()
camera.release()