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