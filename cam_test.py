from imutils.video import VideoStream
import cv2


cap = VideoStream(src=0)
cv2.namedWindow('cam')

while True:
	frame = cap.read()
	cv2.resize(frame, (640, 360))

	cv2.imshow('cam', frame)

	k = cv2.waitKey(1)

	if k & 0xFF == ord('q'):
		break