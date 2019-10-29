from flask import Flask, Response, render_template, request, jsonify
import threading, argparse, datetime, imutils, cv2, time, cfg, os
from keras.preprocessing.image import img_to_array
from socket import gethostbyname, gethostname
from PIL import ImageFont, ImageDraw, Image
from imutils.video import VideoStream, FPS
from keras.models import load_model
from keras import backend as K
from gevent.pywsgi import WSGIServer
from utils import *
import numpy as np

def swish_activation(x):
	return (K.sigmoid(x) * x)

face_detector = cv2.CascadeClassifier(cfg.FRONTAL_FACE_DETECTOR)

emotion_model_path = cfg.MODELS[cfg.CURR_MODEL]
emotion_classifier = load_model(emotion_model_path, 
	custom_objects={"swish_activation": swish_activation}, compile=False)
emotion_classifier._make_predict_function()

input_shape = emotion_classifier.layers[0].input_shape[1:3]

fontpath = cfg.FONT_PATH
font = ImageFont.truetype(fontpath, 32)

outputFrame = None
lock = threading.Lock()

faces = []
emotions = []
tracker_initiated = False
tracker = None
gray = None

app = Flask(__name__)

vs = VideoStream(src=0).start()
time.sleep(2.0)

@app.route("/")
@app.route("/detect")
def index():
	return render_template("detect.html")

@app.route("/quiz")
def quiz():
	return render_template("quiz.html")

@app.route("/get_image_list")
def get_image_list():
	images = os.listdir(cfg.QUIZ_IMAGES_PATH)

	for img in images:
		if img.startswith('.'):
			images.pop(images.index(img))

	return jsonify(images)

@app.route("/get_emotions", methods=["GET"])
def get_emotions():
	if tracker_initiated:
		global emotions
		return jsonify(emotions)
	else:
		return jsonify([])

@app.route("/video_feed")
def video_feed():
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/choose_face", methods=["GET"])
def choose_face():
	global tracker, tracker_initiated, gray, faces

	if not tracker_initiated:
		mX, mY = int(request.args.get("x")), int(request.args.get("y"))
		iW, iH = int(request.args.get("w")), int(request.args.get("h"))

		scale_x = cfg.IN_WIDTH / iW
		scale_y = cfg.IN_HEIGHT / iH

		mX *= scale_x
		mY *= scale_y

		print(mX, mY)
		for x, y, w, h in faces:
			print(x, y, w, h)
			if (x <= mX <= x+w) and (y <= mY <= y+h):
				face_bb = (x, y, w, h)
				tracker = cv2.TrackerMOSSE_create()
				tracker.init(gray, face_bb)
				tracker_initiated = True

	return '1'

@app.route("/reset_face")
def reset_face():
	global tracker_initiated, emotions
	tracker_initiated = False
	emotions = []

	return '1'

def detect_emotion():
	global vs, outputFrame, lock, tracker
	global faces, gray, tracker_initiated
	global emotions

	fps = FPS().start()
	CURRENT_FPS = 0
	frame_ind = 0

	scale_x = cfg.SCALE_WIDTH
	scale_y = cfg.SCALE_HEIGHT

	while True:
		try:
			out_frame = vs.read()
			out_frame = cv2.resize(out_frame, (cfg.OUT_WIDTH, cfg.OUT_HEIGHT))

			gray = cv2.resize(out_frame, (cfg.IN_WIDTH, cfg.IN_HEIGHT))
			gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

			if tracker_initiated:
				success, box = tracker.update(gray)

				if success:
					x, y, w, h = [int(i) for i in box]

					x = 0 if x < 0 else (cfg.IN_WIDTH-1 if x > cfg.IN_WIDTH-1 else x)
					y = 0 if y < 0 else (cfg.IN_HEIGHT-1 if y > cfg.IN_HEIGHT-1 else y)

					roi = gray[y:y+h, x:x+w]
					roi = cv2.resize(roi, input_shape, interpolation=cv2.INTER_AREA)
					roi = roi.astype("float") / 255.0
					roi = img_to_array(roi)
					roi = np.expand_dims(roi, axis=0)
					preds = emotion_classifier.predict(roi)[0]


					emotions = [int(emotion*100) for emotion in preds]

					emotion = np.argmax(preds)

					x, y, w, h = (x//scale_x, y//scale_y, w//scale_x, h//scale_y)
					x, y, w, h = (int(x), int(y), int(w), int(h))

					draw_border(out_frame, (x, y), (x+w, y+h), cfg.SELECTED_COLOR, 3, 5, 30)

					out_frame = Image.fromarray(out_frame)
					draw = ImageDraw.Draw(out_frame)

					tW, tH = font.getsize(cfg.EMOTIONS_RUS[emotion])
					draw.rectangle(((x-2, y+h+5), (x+tW+2, y+h+tH+2)), fill = cfg.SELECTED_COLOR)
					draw.text((x, y+h),  cfg.EMOTIONS_RUS[emotion], font = font, fill = (255, 255, 255, 255))

					out_frame = np.array(out_frame)
				else:
					reset_face()
			else:
				faces = face_detector.detectMultiScale(gray)

				for x, y, w, h in faces:
					x, y, w, h = (x//scale_x, y//scale_y, w//scale_x, h//scale_y)
					x, y, w, h = (int(x), int(y), int(w), int(h))

					draw_border(out_frame, (x, y), (x+w, y+h), cfg.NOT_SELECTED_COLOR, 3, 5, 30)

	        #Draw fps
			draw_text_w_background(out_frame, 'FPS: %.2f' % CURRENT_FPS,
				(20, 20),
				cfg.font, cfg.fontScale,
				cfg.fontColor, cfg.bgColor, 1)

			fps.update()

			if (frame_ind == 10):
				fps.stop()

				CURRENT_FPS = fps.fps()
				fps = FPS().start()
				frame_ind = 0

			# cv2.circle(gray, , 1, (255, 255, 0), -1)
			
			outputFrame = out_frame.copy()

			frame_ind += 1
		except Exception as e:
			print(e)
			continue

def generate():
	global outputFrame, lock

	while True:
		if outputFrame is None:
			continue
		
		(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

		if not flag:
			continue

		yield(b'--frame\r\n' 
			b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')


if __name__ == "__main__":
	t = threading.Thread(target=detect_emotion)
	t.daemon = True
	t.start()

	app.run('0.0.0.0', '80', debug=True, 
		threaded=True, use_reloader=False)
	
	# http_server = WSGIServer(('', 80), app)
	# print(gethostbyname('localhost'))
	# print("Serving on %s" % gethostbyname(gethostname()))
	# http_server.serve_forever()

vs.stop()

