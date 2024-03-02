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
	cv2.rectangle(frame, (100, 100), (1000, 1000), (0, 0, 255), 3)
	
	'''
	now let's try a circle:
	in order, the arguments are:
	frame, center, radius, color (in BGR), line thickness
	'''
	cv2.circle(frame, (250, 520), 45, (0, 255, 0), 2)
	
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