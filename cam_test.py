from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import cv2, imutils

WIDTH, HEIGHT = 640, 360

font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 0.5
fontColor              = (180, 0, 150)
lineType               = 2


cv2.namedWindow('cam')

cap = VideoStream(src=0, resolution=(WIDTH, HEIGHT)).start()
fps = FPS().start()

n_frames = 0

while True:
	frame = cap.read()
	frame = cv2.resize(frame, (WIDTH, HEIGHT))

	fps.update()
	fps.stop()

	cv2.putText(frame, 'FPS: %.2f' % fps.fps(),
					(20, 20),
					font,
					fontScale,
					fontColor,
					lineType)

	cv2.imshow('cam', frame)



	k = cv2.waitKey(1)

	if k & 0xFF == ord('q'):
		break