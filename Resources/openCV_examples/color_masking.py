import cv2
import numpy as np

video = cv2.VideoCapture(0)

while True:
	ret, frame = video.read()

	'''
	to make color masking actually work, we need to convert the image from BGR to HSV (Hue, Saturation, Value)
	'''
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	'''
	specify the range of colors we want to mask, which in this case is red
	'''
	lower_red = np.array([30, 150, 50])
	upper_red = np.array([255, 255, 180])
	
	'''
	now we create the mask, which is an image where anything not in the specified hsv range is black and everything in the range is white.

	the bitwise and applies the mask to the original frame
	'''
	mask = cv2.inRange(hsv, lower_red, upper_red)
	out = cv2.bitwise_and(frame, frame, mask=mask)

	cv2.imshow('masked frame', out) # you can replace out with mask to see the actual mask

	if cv2.waitKey(1) == ord('q'):
		break

video.release()
cv2.destroyAllWindows()