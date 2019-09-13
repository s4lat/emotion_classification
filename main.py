from face_recognition import face_locations
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from imutils.video import VideoStream, FPS
import numpy as np
import cv2

#y0, x0 - left_top
#y1, x1 - right_bottom

WIDTH, HEIGHT = 640, 360

NOT_SELECTED_COLOR = (0, 200, 0)[::-1] #RGB to BGR
SELECTED_COLOR = (255, 140, 0)[::-1]

font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 0.5
fontColor              = (0, 255, 0)[::-1]
lineType               = 2

EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised",
 "neutral"]

MODELS = { 'tiny_x' : 'tiny_exception_0.60_48.hdf5',
 			'mini_x' : 'mini_exception_0.00_64.hdf5',
 			'big_x' : 'big_exception_0.66_48.hdf5',
 			'simpler_cnn' : 'simpler_cnn_62_48.hdf5',
 			'simple_cnn' : 'simple_cnn_0.60_48.hdf5'
 		}

emotion_model_path = "models/%s" % MODELS['big_x']
emotion_classifier = load_model(emotion_model_path, compile=False)

input_shape = emotion_classifier.layers[0].input_shape[1:3]

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

def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1,y1 = pt1
    x2,y2 = pt2

    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)

    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)


cv2.namedWindow('cam')

cap = VideoStream(src=0, resolution=(WIDTH, HEIGHT)).start()

fps = FPS().start()
frame_ind = 0
CURRENT_FPS = 0

while True:
	frame = cap.read()
	frame = cv2.resize(frame, (WIDTH, HEIGHT))
	frame = cv2.flip(frame, 1)

	if tracker_initiated:
		success, box = csrt_tracker.update(frame)

		if success:
			x, y, w, h = [int(i) for i in box]

			x = 0 if x < 0 else (WIDTH-1 if x > WIDTH-1 else x)
			y = 0 if y < 0 else (HEIGHT-1 if y > HEIGHT-1 else y)

			# cv2.rectangle(frame, (x+5, y+5), (x+w, y+h), (0,255,0), 2)
			draw_border(frame, (x, y), (x+w, y+h), SELECTED_COLOR, 2, 5, 10)

			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			roi = gray[y:y+h, x:x+w]
			roi = cv2.resize(roi, input_shape, interpolation=cv2.INTER_AREA)
			roi = roi.astype("float") / 255.0
			roi = img_to_array(roi)
			roi = np.expand_dims(roi, axis=0)
			preds = emotion_classifier.predict(roi)[0]
			emotion = np.argmax(preds)

			cv2.putText(frame, EMOTIONS[emotion] + "_%.f" % (preds[emotion]*100),
					(x+w+10, y+h+10),
					font,
					fontScale,
					fontColor,
					lineType)
			cv2.putText(frame, "Press <C> on your keyboard",
					(10, 15),
					font,
					fontScale,
					fontColor,
					lineType)
			cv2.putText(frame, "if you want to choose other face",
				(10, 30),
					font,
					fontScale,
					fontColor,
					lineType)
		else:
			tracker_initiated = False

	else:
		faces = face_locations(frame)
		cv2.setMouseCallback('cam', choose_face, faces)

		for y0, x1, y1, x0 in faces:
			draw_border(frame, (x0, y0), (x1, y1), NOT_SELECTED_COLOR, 2, 5, 10)

		cv2.putText(frame, "Click on face you want to track",
					(10, 15),
					font,
					fontScale,
					fontColor,
					lineType)

	#Calculate fps
	fps.update()
	frame_ind += 1

	#Refresh CURRENT_FPS every 10 frames
	if (frame_ind == 10):
		fps.stop()
		CURRENT_FPS = fps.fps()
		fps = FPS().start()
		frame_ind = 0

	#Draw fps
	cv2.putText(frame, 'FPS: %.2f' % CURRENT_FPS,
					(20, HEIGHT-20),
					font,
					fontScale,
					fontColor,
					lineType)

	cv2.imshow('cam', frame)

	k = cv2.waitKey(1)

	if k & 0xFF == ord('q'):
		break

	elif k & 0xFF == ord('c'):
		tracker_initiated = False

