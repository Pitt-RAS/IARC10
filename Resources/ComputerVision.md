# RAS Aerial OpenCV Guide

Written by Daniel Hufnagle
(@fuhd on discord)
- blame him for just about anything wrong here unless specified otherwise
# General Tutorial Link
[Official OpenCV Tutorials](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html)
# Getting Started With Webcams
Below is a code segment for getting video working through openCV
```python
import cv2

''' 
declare video input device
using 0 for this tutorial, you may have to change this when running on the jetson
'''
vid = cv2.VideoCapture(0)

'''
main loop:
read the video and show display the frame on screen
'''
while True:
	'''
	ret is irrelevant 99.99999999999999% of the time
	frame is relevant 100% of the time
	'''
	ret, frame = vid.read()
	
	'''
	imshow's first argument is a title that will appear 
	on the window border, name it whatever the hell you want
	'''
	
	cv2.imshow('webcam feed!', frame)
	
	'''
	terminate the program if you hit the q key
	'''
	if cv2.waitKey(1) == ord('q'):
		break

'''
termination:
this may have to be put in a loop that iterates a couple times.
I don't know why, but sometimes it just be like that.
Generally, should work as normal though
'''
vid.release()
cv2.destroyAllWindows()
```
# Drawing On A Frame
[Official drawing tutorials may have a little more in depth](https://docs.opencv.org/3.4/dc/da5/tutorial_py_drawing_functions.html)
```python
import cv2

vid = cv2.VideoCapture(0)

while True:
	ret, frame = vid.read()
	
	'''
	let's draw a rectangle:
	in order, the arguments are:
	frame, starting coordinates, ending coordinates, color (in BGR),
	line thickness
	'''
	cv2.rectangle(frame, (10, 10), (100, 100), (0, 0, 255), 3)
	
	'''
	now let's try a circle:
	in order, the arguments are:
	frame, center, radius, color (in BGR), line thickness
	'''
	cv2.circle(frame, (20, 20), 15, (0, 255, 0), 2)
	
	'''
	text is also pretty cool:
	in order, the arguments are:
	frame, text, origin, font, fontScale, color, thickness
	'''
	cv2.putText(frame, 'hello!', (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 0), 2)
	
	cv2.imshow('now theres shit here', frame)
	if cv2.waitKey(1) == ord('q'):
		break

vid.release()
cv2.destroyAllWindows()
```
# Haar Cascading Classifiers
This is in the event that we have the worst case scenario where we can't get a deep learning model working in time. It could also prove useful for testing other things before we have a more accurate model. However, this will only work if we need something like face or body detection that is already premade for us. Otherwise, training a Haar Cascade might end up being equally if not more painful than a neural network.

[Here's the link to all the classifier xml files](https://github.com/opencv/opencv/tree/master/data/haarcascades)

[Here'a another link to everything about Haar Cascades. It is confusing as hell and almost completely unnecessary, but you do you](https://medium.com/analytics-vidhya/haar-cascades-explained-38210e57970d)
```python
import cv2

'''
declare our cascading classifiers
we just pass the xml file in as the argument
yes, it is that simple

if you want full body detection, you're going to have to go to the github repo with all the classifiers and get the proper xml file
'''
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

video = cv2.VideoCapture(0)

while True:
	ret, frame = video.read()
	
	'''
	things are faster (at least for the classifiers we have)
	if they are in grayscale, so we create a new image that
	is just our old frame grayscaled
	'''
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	'''
	now comes the fun part:
	all the detection is just one line of code
	however, this line is the biggest pain in the ass
	the arguments are:
	the frame, scale factor, and minimum number of neighbors.
	
	These numbers need to be tweaked to adjust sensitivity.
	It differs from camera to camera.
	The official definitions are as follows:
	
	Scale Factor:
		specifies how much the image size is reduced at each image scale
		
		the important things are:
		higher numbers are faster detection, but lower 
		reduces sensitivity
			this isn't necessarily a bad thing
			because Haar Cascades can very easily overdetect
	Minimum Neighbors:
		specifies how many neighbors each candidate rectangle should
		have to retain it
		
		the important things are:
		higher number is going to give less detections,
		but higher quality detections
	
	Honestly, just play around until you find something that works
	'''
	faces = face_cascade.detectMultiScale(gray, 1.1, 8)
	
	num_faces = 0
	num_smiles = 0
	
	'''
	the detectMultiScale returns a list of tuples containing the
	coordinates of all detected faces (well, the top left corner, 
	width, and height)
	
	now we just iterate through this list and draw rectangles around
	them
	'''
	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
		
		'''
		now we are going to create smaller subframes to run smile
		detection on
		'''
		face_gray = gray[y:y+h, x:x+w]
		face_frame = frame[y:y+h, x:x+w]
		
		num_faces += 1
		
		'''
		this is repeating the face detection code but on the subframes
		created above. We are now detecting smiles.
		'''
		smiles = smile_cascade.detectMultiScale(face_gray, 1.8, 40)
		for (sx, sy, sw, sh) in smiles:
			cv2.rectangle(face_frame, (sx, sy), (sx+sw, sy+sh), (0, 0, 255), 2)
			num_smiles += 1
	
	is_smiling = 'Not smiling'
	if num_smiles >= num_faces:
		is_smiling = 'Smiling'	
	cv2.putText(frame, is_smiling, fontFace=cv2.FONT_HERSHEY_SIMPLEX, org=(10, 30), fontScale=1.1, color=(255, 255, 0))
	
	cv2.imshow('webcam', frame)
	if cv2.waitKey(1) == ord('q'):
		break

video.release()
cv2.destroyAllWindows()
```
