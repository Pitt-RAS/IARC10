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