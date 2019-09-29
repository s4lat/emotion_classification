# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'templates_ui/testWidget.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!
from keras.preprocessing.image import img_to_array
from imutils.face_utils.helpers import rect_to_bb
from PIL import ImageFont, ImageDraw, Image
from imutils.video import VideoStream, FPS
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import queue, threading, cv2
from utils import *
import numpy as np

class FrameWidget(QWidget):
    def __init__(self, parent=None):
        super(FrameWidget, self).__init__(parent)
        self.parent = parent
        self.cam_frame = None

        self.mousePressEvent = self.click

    def set_frame(self, frame):
        self.cam_frame = frame
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.cam_frame:
            qp.drawImage(QPoint(0, 0), self.cam_frame)

        qp.end()


    def click(self, event):
        coords = event.pos()
        coords = (coords.x(), coords.y())
        self.parent.chooseFace(coords)

class DetectWidget(QWidget):
    def __init__(self, cfg, face_detector, emotion_classifier, parent=None):
        super(DetectWidget, self).__init__(parent)

        self.cfg = cfg

        if self.cfg.USE_HOG:
            from dlib import get_frontal_face_detector
            self.face_detector = get_frontal_face_detector()
        else:
            self.face_detector = face_detector

        self.emotion_classifier = emotion_classifier

        self.faces = []
        self.tracker_initiated = False
        self.gray = None

        self.running = True
        self.q = queue.Queue()

        self.capture_thread = threading.Thread(target=self.grab, args = (0, self.q))
        self.capture_thread.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_widget)
        self.timer.start(1)

        self.setupUi(self)
        self.last_setup_ui()

    def chooseFace(self, coords):
        mX, mY = coords

        OUT_WIDTH = self.camForm.frameGeometry().width()
        OUT_HEIGHT = self.camForm.frameGeometry().height()

        scale_x = self.cfg.IN_WIDTH / OUT_WIDTH
        scale_y = self.cfg.IN_HEIGHT / OUT_HEIGHT

        mX *= scale_x
        mY *= scale_y

        if not self.tracker_initiated:
            for x, y, w, h in self.faces:
                if (x <= mX <= x+w) and (y <= mY <= y+h):
                    face_bb = (x, y, w, h)
                    self.tracker = cv2.TrackerMOSSE_create()
                    self.tracker.init(self.gray, face_bb)
                    self.tracker_initiated = True
                    self.resetBtn.setEnabled(True)

    def resetFace(self):
        self.tracker_initiated = False
        self.resetBtn.setEnabled(False)

    def grab(self, cam, queue):
        try:
            cap = VideoStream(src=0).start()
            input_shape = self.emotion_classifier.layers[0].input_shape[1:3]

            self.tracker_initiated = False

            fontpath = "static/helvetica.ttf"
            font = ImageFont.truetype(fontpath, 24)

            fps = FPS().start()
            frame_ind = 0
            CURRENT_FPS = 0
            emotions = [0] * 7

            self.camLabel.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:24pt;\">Камера</span></p></body></html>")

            while (self.running):
                OUT_WIDTH = self.camForm.frameGeometry().width()
                OUT_HEIGHT = self.camForm.frameGeometry().height()

                scale_x = self.cfg.IN_WIDTH / OUT_WIDTH
                scale_y = self.cfg.IN_HEIGHT / OUT_HEIGHT

                frame = cap.read()
                frame = cv2.flip(frame, 1)

                gray = cv2.resize(frame, (self.cfg.IN_WIDTH, self.cfg.IN_HEIGHT))
                gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

                out_frame = cv2.resize(frame, (OUT_WIDTH, OUT_HEIGHT))

                self.gray = gray

                if self.tracker_initiated:
                    success, box = self.tracker.update(gray)

                    if success:
                        x, y, w, h = [int(i) for i in box]

                        x = 0 if x < 0 else (self.cfg.IN_WIDTH-1 if x > self.cfg.IN_WIDTH-1 else x)
                        y = 0 if y < 0 else (self.cfg.IN_HEIGHT-1 if y > self.cfg.IN_HEIGHT-1 else y)

                        roi = gray[y:y+h, x:x+w]
                        roi = cv2.resize(roi, input_shape, interpolation=cv2.INTER_AREA)

                        roi = roi.astype("float") / 255.0
                        roi = img_to_array(roi)
                        roi = np.expand_dims(roi, axis=0)
                        preds = self.emotion_classifier.predict(roi)[0]
                        emotions = [int(emotion*100) for emotion in preds]
                        emotion = np.argmax(preds)

                        x, y, w, h = (x//scale_x, y//scale_y, w//scale_x, h//scale_y)
                        x, y, w, h = (int(x), int(y), int(w), int(h))

                        draw_border(out_frame, (x, y), (x+w, y+h), self.cfg.SELECTED_COLOR, 2, 5, 15)

                        out_frame = Image.fromarray(out_frame)
                        draw = ImageDraw.Draw(out_frame)

                        tW, tH = font.getsize(self.cfg.EMOTIONS_RUS[emotion])
                        draw.rectangle(((x-2, y+h+5), (x+tW+2, y+h+tH+2)), fill = self.cfg.SELECTED_COLOR)
                        draw.text((x, y+h),  self.cfg.EMOTIONS_RUS[emotion], font = font, fill = (255, 255, 255, 255))

                        out_frame = np.array(out_frame)

                    else:
                        self.resetFace()

                else:
                    if self.cfg.USE_HOG:
                        faces = self.face_detector(gray)
                        self.faces = [rect_to_bb(rect) for rect in faces]
                    else:
                        self.faces = self.face_detector.detectMultiScale(gray)

                    for x, y, w, h in self.faces:
                        x, y, w, h = (x//scale_x, y//scale_y, w//scale_x, h//scale_y)
                        x, y, w, h = (int(x), int(y), int(w), int(h))

                        draw_border(out_frame, (x, y), (x+w, y+h), self.cfg.NOT_SELECTED_COLOR, 2, 5, 15)

                #Draw fps
                draw_text_w_background(out_frame, 'FPS: %.2f' % CURRENT_FPS,
                        (20, 20),
                        self.cfg.font, self.cfg.fontScale,
                        self.cfg.fontColor, self.cfg.bgColor, 1)

                if queue.qsize() < 10:
                    #Calculate fps
                    fps.update()
                    frame_ind += 1
                    #Refresh CURRENT_FPS every 10 frames
                    if (frame_ind == 10):
                        fps.stop()
                        CURRENT_FPS = fps.fps()
                        fps = FPS().start()
                        frame_ind = 0

                    result = {'img' : out_frame, 'emotions': emotions if self.tracker_initiated else [0]*7}

                    queue.put(result)
        except Exception as e:
            print(e)
            
        finally:
            cap.stop()

    def update_widget(self):
        if not self.q.empty():
            #Update camForm
            data = self.q.get()
            img = cv2.cvtColor(data["img"], cv2.COLOR_BGR2RGB)

            height, width, bpc = img.shape
            bpl = bpc * width
            img = QImage(img, width, height, bpl, QImage.Format_RGB888)
            self.camForm.set_frame(img)

            #Update progress bars
            EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised",
 "neutral"]

            self.angryBar.setProperty("value", data['emotions'][0])
            self.disgustBar.setProperty("value", data['emotions'][1])
            self.scaredBar.setProperty("value", data['emotions'][2])
            self.happyBar.setProperty("value", data['emotions'][3])
            self.sadBar.setProperty("value", data['emotions'][4])
            self.surpriseBar.setProperty("value", data['emotions'][5])
            self.neutralBar.setProperty("value", data['emotions'][6])

    def closeEvent(self, event):
        self.running = False

    def last_setup_ui(self):
        self.resetBtn.clicked.connect(self.resetFace)

        if QIcon.hasThemeIcon('leftarrow-icon'):
            self.backBtn.setIcon(QIcon.fromTheme('leftarrow-icon'))
        else:
            self.backBtn.setText("←")

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(985, 584)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.backBtn = QPushButton(Form)
        self.backBtn.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backBtn.sizePolicy().hasHeightForWidth())
        self.backBtn.setSizePolicy(sizePolicy)
        self.backBtn.setMinimumSize(QSize(64, 64))
        self.backBtn.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(32)
        self.backBtn.setFont(font)
        self.backBtn.setLayoutDirection(Qt.LeftToRight)
        self.backBtn.setStyleSheet("")
        self.backBtn.setObjectName("backBtn")
        self.gridLayout.addWidget(self.backBtn, 1, 0, 1, 1)
        self.camLabel = QLabel(Form)
        self.camLabel.setMinimumSize(QSize(0, 48))
        self.camLabel.setMaximumSize(QSize(16777215, 16777215))
        self.camLabel.setStyleSheet("border: 2px solid gray;\n"
"background: rgb(240, 240, 240)")
        self.camLabel.setObjectName("camLabel")
        self.gridLayout.addWidget(self.camLabel, 1, 1, 1, 1)
        self.label_2 = QLabel(Form)
        self.label_2.setMaximumSize(QSize(250, 16777215))
        self.label_2.setStyleSheet("border: 2px solid gray;\n"
"background: rgb(240, 240, 240)")
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 3, 1, 1)
        self.resetBtn = QPushButton(Form)
        self.resetBtn.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resetBtn.sizePolicy().hasHeightForWidth())
        self.resetBtn.setSizePolicy(sizePolicy)
        self.resetBtn.setMinimumSize(QSize(150, 50))
        self.resetBtn.setMaximumSize(QSize(16777215, 80))
        font = QFont()
        font.setPointSize(16)
        self.resetBtn.setFont(font)
        self.resetBtn.setObjectName("resetBtn")
        self.gridLayout.addWidget(self.resetBtn, 5, 1, 1, 1)
        self.camForm = FrameWidget(Form)
        self.camForm.setMinimumSize(QSize(640, 360))
        self.camForm.setMaximumSize(QSize(16777215, 16777215))
        self.camForm.setStyleSheet("border: 2px solid gray;\n"
"background: rgb(240, 240, 240)")
        self.camForm.setObjectName("camForm")
        self.gridLayout.addWidget(self.camForm, 4, 1, 1, 1)
        self.predsWidget = QWidget(Form)
        self.predsWidget.setMaximumSize(QSize(250, 16777215))
        self.predsWidget.setStyleSheet("#predsWidget {\n"
"    border: 2px solid gray;\n"
"    background: rgb(240, 240, 240)\n"
"}")
        self.predsWidget.setObjectName("predsWidget")
        self.verticalLayout_2 = QVBoxLayout(self.predsWidget)
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, 12)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.happyLabel = QLabel(self.predsWidget)
        self.happyLabel.setMaximumSize(QSize(16777215, 32))
        font = QFont()
        font.setPointSize(16)
        self.happyLabel.setFont(font)
        self.happyLabel.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.happyLabel.setObjectName("happyLabel")
        self.verticalLayout_2.addWidget(self.happyLabel)
        self.happyBar = QProgressBar(self.predsWidget)
        self.happyBar.setMinimumSize(QSize(150, 16))
        self.happyBar.setMaximumSize(QSize(16777215, 35))
        self.happyBar.setStyleSheet("QProgressBar{\n"
"    background-color: rgb(245, 245, 245);\n"
"    border: 2px solid black;\n"
"    border-radius: 5px;\n"
"    text-align: center\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"     background-color: #FFA52C;\n"
" }")
        self.happyBar.setProperty("value", 24)
        self.happyBar.setAlignment(Qt.AlignCenter)
        self.happyBar.setObjectName("happyBar")
        self.verticalLayout_2.addWidget(self.happyBar)
        self.surpriseLabel = QLabel(self.predsWidget)
        self.surpriseLabel.setMaximumSize(QSize(16777215, 32))
        font = QFont()
        font.setPointSize(16)
        self.surpriseLabel.setFont(font)
        self.surpriseLabel.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.surpriseLabel.setObjectName("surpriseLabel")
        self.verticalLayout_2.addWidget(self.surpriseLabel)
        self.surpriseBar = QProgressBar(self.predsWidget)
        self.surpriseBar.setMinimumSize(QSize(150, 16))
        self.surpriseBar.setMaximumSize(QSize(16777215, 35))
        self.surpriseBar.setStyleSheet("QProgressBar{\n"
"    background-color: rgb(245, 245, 245);\n"
"    border: 2px solid black;\n"
"    border-radius: 5px;\n"
"    text-align: center\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"     background-color: #FFFF41;\n"
" }")
        self.surpriseBar.setProperty("value", 24)
        self.surpriseBar.setAlignment(Qt.AlignCenter)
        self.surpriseBar.setObjectName("surpriseBar")
        self.verticalLayout_2.addWidget(self.surpriseBar)
        self.neutralLabel = QLabel(self.predsWidget)
        self.neutralLabel.setMaximumSize(QSize(16777215, 32))
        font = QFont()
        font.setPointSize(16)
        self.neutralLabel.setFont(font)
        self.neutralLabel.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.neutralLabel.setObjectName("neutralLabel")
        self.verticalLayout_2.addWidget(self.neutralLabel)
        self.neutralBar = QProgressBar(self.predsWidget)
        self.neutralBar.setMinimumSize(QSize(150, 16))
        self.neutralBar.setMaximumSize(QSize(16777215, 35))
        self.neutralBar.setStyleSheet("QProgressBar{\n"
"    background-color: rgb(245, 245, 245);\n"
"    border: 2px solid black;\n"
"    border-radius: 5px;\n"
"    text-align: center\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"     background-color: #008018;\n"
" }")
        self.neutralBar.setProperty("value", 24)
        self.neutralBar.setAlignment(Qt.AlignCenter)
        self.neutralBar.setObjectName("neutralBar")
        self.verticalLayout_2.addWidget(self.neutralBar)
        self.sadLabel = QLabel(self.predsWidget)
        self.sadLabel.setMaximumSize(QSize(16777215, 32))
        font = QFont()
        font.setPointSize(16)
        self.sadLabel.setFont(font)
        self.sadLabel.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.sadLabel.setObjectName("sadLabel")
        self.verticalLayout_2.addWidget(self.sadLabel)
        self.sadBar = QProgressBar(self.predsWidget)
        self.sadBar.setMinimumSize(QSize(150, 16))
        self.sadBar.setMaximumSize(QSize(16777215, 35))
        self.sadBar.setStyleSheet("QProgressBar{\n"
"    background-color: rgb(245, 245, 245);\n"
"    border: 2px solid black;\n"
"    border-radius: 5px;\n"
"    text-align: center\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"     background-color: rgb(0, 93, 255);\n"
" }")
        self.sadBar.setProperty("value", 24)
        self.sadBar.setAlignment(Qt.AlignCenter)
        self.sadBar.setObjectName("sadBar")
        self.verticalLayout_2.addWidget(self.sadBar)
        self.scaredLabel = QLabel(self.predsWidget)
        self.scaredLabel.setMaximumSize(QSize(16777215, 32))
        font = QFont()
        font.setPointSize(16)
        self.scaredLabel.setFont(font)
        self.scaredLabel.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.scaredLabel.setObjectName("scaredLabel")
        self.verticalLayout_2.addWidget(self.scaredLabel)
        self.scaredBar = QProgressBar(self.predsWidget)
        self.scaredBar.setMinimumSize(QSize(150, 16))
        self.scaredBar.setMaximumSize(QSize(16777215, 35))
        self.scaredBar.setStyleSheet("QProgressBar{\n"
"    background-color: rgb(245, 245, 245);\n"
"    border: 2px solid black;\n"
"    border-radius: 5px;\n"
"    text-align: center\n"
"}\n"
"\n"
"\n"
"QProgressBar::chunk {\n"
"     background-color: #86007D;\n"
" }")
        self.scaredBar.setProperty("value", 24)
        self.scaredBar.setAlignment(Qt.AlignCenter)
        self.scaredBar.setObjectName("scaredBar")
        self.verticalLayout_2.addWidget(self.scaredBar)
        self.disgustLabel = QLabel(self.predsWidget)
        self.disgustLabel.setMaximumSize(QSize(16777215, 32))
        font = QFont()
        font.setPointSize(16)
        self.disgustLabel.setFont(font)
        self.disgustLabel.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.disgustLabel.setObjectName("disgustLabel")
        self.verticalLayout_2.addWidget(self.disgustLabel)
        self.disgustBar = QProgressBar(self.predsWidget)
        self.disgustBar.setMinimumSize(QSize(150, 16))
        self.disgustBar.setMaximumSize(QSize(16777215, 35))
        self.disgustBar.setStyleSheet("QProgressBar{\n"
"    background-color: rgb(245, 245, 245);\n"
"    border: 2px solid black;\n"
"    border-radius: 5px;\n"
"    text-align: center\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"     background-color: #7F370A;\n"
" }")
        self.disgustBar.setProperty("value", 24)
        self.disgustBar.setAlignment(Qt.AlignCenter)
        self.disgustBar.setObjectName("disgustBar")
        self.verticalLayout_2.addWidget(self.disgustBar)
        self.angryLabel = QLabel(self.predsWidget)
        self.angryLabel.setMaximumSize(QSize(16777215, 32))
        font = QFont()
        font.setPointSize(16)
        self.angryLabel.setFont(font)
        self.angryLabel.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.angryLabel.setObjectName("angryLabel")
        self.verticalLayout_2.addWidget(self.angryLabel)
        self.angryBar = QProgressBar(self.predsWidget)
        self.angryBar.setMinimumSize(QSize(150, 16))
        self.angryBar.setMaximumSize(QSize(16777215, 35))
        self.angryBar.setStyleSheet("QProgressBar{\n"
"    background-color: rgb(245, 245, 245);\n"
"    border: 2px solid black;\n"
"    border-radius: 5px;\n"
"    text-align: center\n"
"}\n"
" \n"
"QProgressBar::chunk {\n"
"     background-color: #FF0018;\n"
" }")
        self.angryBar.setProperty("value", 24)
        self.angryBar.setAlignment(Qt.AlignCenter)
        self.angryBar.setObjectName("angryBar")
        self.verticalLayout_2.addWidget(self.angryBar)
        self.gridLayout.addWidget(self.predsWidget, 4, 3, 1, 1)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.camLabel.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:24pt;\">Камера(загрузка...)</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:24pt;\">Эмоции</span></p></body></html>"))
        self.resetBtn.setText(_translate("Form", "Выбрать другое лицо"))
        self.happyLabel.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Счастье</span></p></body></html>"))
        self.surpriseLabel.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Удивление</span></p></body></html>"))
        self.neutralLabel.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Спокойствие</span></p></body></html>"))
        self.sadLabel.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Грусть</span></p></body></html>"))
        self.scaredLabel.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Испуг</span></p></body></html>"))
        self.disgustLabel.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Отвращение</span></p></body></html>"))
        self.angryLabel.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Злость</span></p></body></html>"))



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = DetectWidget()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
