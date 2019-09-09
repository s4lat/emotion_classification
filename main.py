from face_recognition import face_locations
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from imutils.video import VideoStream
import imutils
import numpy as np
import cv2, math

#y0, x0 - left_top
#y1, x1 - right_bottom
WIDTH, HEIGHT = 640, 360
input_shape = (64, 64)
font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 0.7
fontColor              = (180,0,255)
lineType               = 2


emotion_model_path = "models/mini_exception_0.00_64.hdf5"
EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised",
 "neutral"]
emotion_classifier = load_model(emotion_model_path, compile=False)

csrt_tracker = None
tracker_initiated = False

def choose_face(event, mX, mY, flags, faces):
	global tracker_initiated, csrt_tracker

	if not tracker_initiated:
		if event == cv2.EVENT_LBUTTONUP and faces:
			for y0, x1, y1, x0 in faces:
				if (x0 <= mX <= x1) and (y0 <= mY <= y1):
					face_bb = (x0, y0, x1-x0, y1-y0)
					csrt_tracker = cv2.TrackerCSRT_create()
					csrt_tracker.init(frame, face_bb)
					tracker_initiated = True



cap = VideoStream(src=0).start()
cv2.namedWindow('cam')

while True:
	frame = cap.read()
	frame = cv2.resize(frame, (WIDTH, HEIGHT))
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


	if tracker_initiated:
		success, box = csrt_tracker.update(frame)

		if success:
			x, y, w, h = [int(i) for i in box]

			x = 0 if x < 0 else (WIDTH-1 if x > WIDTH-1 else x)
			y = 0 if y < 0 else (HEIGHT-1 if y > HEIGHT-1 else y)


			cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

			roi = gray[y:y+h, x:x+w]
			roi = cv2.resize(roi, input_shape)
			roi = roi.astype("float") / 255.0
			roi = img_to_array(roi)
			roi = np.expand_dims(roi, axis=0)
			preds = emotion_classifier.predict(roi)[0]
			emotion = np.argmax(preds)

			cv2.putText(frame, EMOTIONS[emotion] + "_%.f" % (preds[emotion]*100),
					(x+w, y+h),
					font,
					fontScale,
					fontColor,
					lineType)
		else:
			print('Face dissapear!!')
			print('Choose new face')
			tracker_initiated = False

	else:
		faces = face_locations(frame)
		cv2.setMouseCallback('cam', choose_face, faces)

		for y0, x0, y1, x1 in faces:
			cv2.rectangle(frame, (x0, y0), (x1, y1), (0,255,0), 2)
			

			

			# cv2.rectangle(frame, (x0, y0), (x1, y1), (0,255,0), 3)

	cv2.imshow('cam', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

