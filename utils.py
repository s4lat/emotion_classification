import cv2

#Рисование рамки со скругленными уголками
def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1,y1 = pt1
    x2,y2 = pt2

    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness, cv2.LINE_AA)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness, cv2.LINE_AA)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness, cv2.LINE_AA)

    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness, cv2.LINE_AA)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness, cv2.LINE_AA)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness, cv2.LINE_AA)

    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness, cv2.LINE_AA)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness, cv2.LINE_AA)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness, cv2.LINE_AA)

    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness, cv2.LINE_AA)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness, cv2.LINE_AA)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness, cv2.LINE_AA)

#Рисование текста с фоном
def draw_text_w_background(img, text, coords, font, fontScale, fontColor, bgColor, thickness):
	lines = text.split("\n")
	(x, y) = coords

	for i, line in enumerate(lines):
		(w, h) = cv2.getTextSize(line, font, fontScale=fontScale, thickness=thickness)[0]
		y = coords[1] + h*i
		cv2.rectangle(img, (x-5, y-h), (x+w+5, y+5), bgColor, cv2.FILLED)

	h += 2
	for i, line in enumerate(lines):
		y = coords[1] + h*i
		cv2.putText(img, line, (x, y), font, fontScale, fontColor, thickness, cv2.LINE_AA)

def detect_emotion():
    global vs, outputFrame, lock

    fps = FPS().start()
    CURRENT_FPS = 0
    frame_ind = 0
    while True:
        out_frame = vs.read()
        
        OUT_WIDTH = out_frame.shape[1]
        OUT_HEIGHT = out_frame.shape[0]

        gray = cv2.resize(out_frame, (cfg.IN_WIDTH, cfg.IN_HEIGHT))
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

        scale_x = cfg.IN_WIDTH / OUT_WIDTH
        scale_y = cfg.IN_HEIGHT / OUT_HEIGHT

        faces = face_detector.detectMultiScale(gray)

        for x, y, w, h in faces:
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

            draw_border(out_frame, (x, y), (x+w, y+h), cfg.SELECTED_COLOR, 2, 5, 15)

            out_frame = Image.fromarray(out_frame)
            draw = ImageDraw.Draw(out_frame)

            tW, tH = font.getsize(cfg.EMOTIONS_RUS[emotion])
            draw.rectangle(((x-2, y+h+5), (x+tW+2, y+h+tH+2)), fill = cfg.SELECTED_COLOR)
            draw.text((x, y+h),  cfg.EMOTIONS_RUS[emotion], font = font, fill = (255, 255, 255, 255))

            out_frame = np.array(out_frame)

        #Draw fps
        draw_text_w_background(out_frame, 'FPS: %.2f' % CURRENT_FPS,
            (20, 20),
            cfg.font, cfg.fontScale,
            cfg.fontColor, cfg.bgColor, 1)

        with lock:
            fps.update()

            if (frame_ind == 10):
                fps.stop()

                CURRENT_FPS = fps.fps()
                fps = FPS().start()
                frame_ind = 0

            outputFrame = out_frame.copy()

        frame_ind += 1