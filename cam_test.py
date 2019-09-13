from imutils.video import VideoStream, FPS
import cv2

WIDTH, HEIGHT = 640, 360

font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 0.5
fontColor              = (180, 0, 150)
lineType               = 2

cv2.namedWindow('cam')

cap = VideoStream(src=0, resolution=(WIDTH, HEIGHT)).start()

fps = FPS().start()
frame_ind = 0
CURRENT_FPS = 0

while True:
	frame = cap.read()
	frame = cv2.resize(frame, (WIDTH, HEIGHT))
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#Calculate fps
	fps.update()
	frame_ind += 1

	#Refresh CURRENT_FPS every 10 frames
	if (frame_ind == 10):
		fps.stop()
		CURRENT_FPS = fps.fps()
		fps = FPS().start()
		frame_ind = 0

	cv2.putText(frame, 'FPS: %.2f' % CURRENT_FPS,
					(20, 20),
					font,
					fontScale,
					fontColor,
					lineType)

	cv2.imshow('cam', frame)



	k = cv2.waitKey(1)

	if k & 0xFF == ord('q'):
		break