# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'templates_ui/testWidget.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!
from keras.preprocessing.image import img_to_array
from imutils.video import VideoStream, FPS
from imutils.face_utils.helpers import rect_to_bb
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

class TestWidget(QWidget):
    def __init__(self, cfg, face_detector, emotion_classifier, parent=None):
        super(TestWidget, self).__init__(parent)

        self.cfg = cfg

        if self.cfg.USE_HOG:
            from dlib import get_frontal_face_detector
            self.face_detector = get_frontal_face_detector()
        else:
            self.face_detector = face_detector

        self.emotion_classifier = emotion_classifier

        self.faces = None
        self.tracker_initiated = False
        self.gray = None

        self.running = True
        self.q = queue.Queue()

        self.capture_thread = threading.Thread(target=self.grab, args = (0, self.q, self.cfg.OUT_WIDTH, self.cfg.OUT_HEIGHT))
        self.capture_thread.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_widget)
        self.timer.start(1)

        self.setupUi(self);

    def chooseFace(self, coords):
        mX, mY = coords
        if not self.tracker_initiated:
            mX, mY = (mX//self.cfg.SCALE_FACTOR, mY//self.cfg.SCALE_FACTOR)
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


    def grab(self, cam, queue, width, height):
        try:
            cap = VideoStream(src=0).start()
            input_shape = self.emotion_classifier.layers[0].input_shape[1:3]

            self.tracker_initiated = False

            fps = FPS().start()
            frame_ind = 0
            CURRENT_FPS = 0
            emotions = [0] * 7

            self.camLabel.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:24pt;\">Камера</span></p></body></html>")

            while (self.running):
                out_frame = cap.read()
                out_frame = cv2.resize(out_frame, (self.cfg.OUT_WIDTH, self.cfg.OUT_HEIGHT))
                out_frame = cv2.flip(out_frame, 1)

                frame = cv2.resize(out_frame, (self.cfg.IN_WIDTH, self.cfg.IN_HEIGHT))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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

                        x, y, w, h = (x*self.cfg.SCALE_FACTOR, y*self.cfg.SCALE_FACTOR, w*self.cfg.SCALE_FACTOR, h*self.cfg.SCALE_FACTOR)
                        x, y, w, h = (int(x), int(y), int(w), int(h))

                        draw_border(out_frame, (x, y), (x+w, y+h), self.cfg.SELECTED_COLOR, 2, 5, 10)
                    else:
                        self.tracker_initiated = False

                else:
                    if self.cfg.USE_HOG:
                        faces = self.face_detector(gray)
                        self.faces = [rect_to_bb(rect) for rect in faces]
                    else:
                        self.faces = self.face_detector.detectMultiScale(gray)

                    for x, y, w, h in self.faces:
                        x, y, w, h = (x*self.cfg.SCALE_FACTOR, y*self.cfg.SCALE_FACTOR, w*self.cfg.SCALE_FACTOR, h*self.cfg.SCALE_FACTOR)
                        x, y, w, h = (int(x), int(y), int(w), int(h))

                        draw_border(out_frame, (x, y), (x+w, y+h), self.cfg.NOT_SELECTED_COLOR, 2, 5, 10)

                    # cv2.setMouseCallback('cam', choose_face, faces)

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

                    result = {'img' : out_frame, 'emotions': emotions}

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


    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(854, 577)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(854, 577))
        Form.setMaximumSize(QSize(854, 610))
        Form.setLayoutDirection(Qt.LeftToRight)
        Form.setAutoFillBackground(False)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(12, 12, 12, 100)
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.backBtn = QPushButton(Form)
        self.backBtn.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backBtn.sizePolicy().hasHeightForWidth())
        self.backBtn.setSizePolicy(sizePolicy)
        self.backBtn.setMinimumSize(QSize(64, 64))
        self.backBtn.setMaximumSize(QSize(64, 64))
        font = QFont()
        font.setPointSize(32)
        self.backBtn.setFont(font)
        self.backBtn.setLayoutDirection(Qt.LeftToRight)
        self.backBtn.setStyleSheet("")
        self.backBtn.setObjectName("backBtn")
        self.horizontalLayout_2.addWidget(self.backBtn)
        self.camLabel = QLabel(Form)
        self.camLabel.setMinimumSize(QSize(0, 43))
        self.camLabel.setMaximumSize(QSize(16777215, 43))
        self.camLabel.setStyleSheet("border: 2px solid gray;\n"
"")
        self.camLabel.setObjectName("camLabel")
        self.horizontalLayout_2.addWidget(self.camLabel)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 3, 1, 1)
        self.label = QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 4, 1, 1)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.camForm = FrameWidget(Form)
        self.camForm.setMinimumSize(QSize(640, 360))
        self.camForm.setMaximumSize(QSize(640, 360))
        self.camForm.setStyleSheet("border: 2px solid gray")
        self.camForm.setObjectName("camForm")
        self.gridLayout.addWidget(self.camForm, 4, 3, 1, 1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 0, 10, 30)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.happyLabel = QLabel(Form)
        self.happyLabel.setMaximumSize(QSize(150, 32))
        font = QFont()
        font.setPointSize(16)
        self.happyLabel.setFont(font)
        self.happyLabel.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.happyLabel.setObjectName("happyLabel")
        self.verticalLayout.addWidget(self.happyLabel)
        self.happyBar = QProgressBar(Form)
        self.happyBar.setMinimumSize(QSize(150, 16))
        self.happyBar.setMaximumSize(QSize(150, 20))
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
        self.happyBar.setObjectName("happyBar")
        self.verticalLayout.addWidget(self.happyBar)
        self.surpriseLabel = QLabel(Form)
        self.surpriseLabel.setMaximumSize(QSize(150, 32))
        font = QFont()
        font.setPointSize(16)
        self.surpriseLabel.setFont(font)
        self.surpriseLabel.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.surpriseLabel.setObjectName("surpriseLabel")
        self.verticalLayout.addWidget(self.surpriseLabel)
        self.surpriseBar = QProgressBar(Form)
        self.surpriseBar.setMinimumSize(QSize(150, 16))
        self.surpriseBar.setMaximumSize(QSize(150, 20))
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
        self.surpriseBar.setObjectName("surpriseBar")
        self.verticalLayout.addWidget(self.surpriseBar)
        self.neutralLabel = QLabel(Form)
        self.neutralLabel.setMaximumSize(QSize(150, 32))
        font = QFont()
        font.setPointSize(16)
        self.neutralLabel.setFont(font)
        self.neutralLabel.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.neutralLabel.setObjectName("neutralLabel")
        self.verticalLayout.addWidget(self.neutralLabel)
        self.neutralBar = QProgressBar(Form)
        self.neutralBar.setMinimumSize(QSize(150, 16))
        self.neutralBar.setMaximumSize(QSize(150, 20))
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
        self.neutralBar.setObjectName("neutralBar")
        self.verticalLayout.addWidget(self.neutralBar)
        self.sadLabel = QLabel(Form)
        self.sadLabel.setMaximumSize(QSize(150, 32))
        font = QFont()
        font.setPointSize(16)
        self.sadLabel.setFont(font)
        self.sadLabel.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.sadLabel.setObjectName("sadLabel")
        self.verticalLayout.addWidget(self.sadLabel)
        self.sadBar = QProgressBar(Form)
        self.sadBar.setMinimumSize(QSize(150, 16))
        self.sadBar.setMaximumSize(QSize(150, 20))
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
        self.sadBar.setObjectName("sadBar")
        self.verticalLayout.addWidget(self.sadBar)
        self.scaredLabel = QLabel(Form)
        self.scaredLabel.setMaximumSize(QSize(150, 32))
        font = QFont()
        font.setPointSize(16)
        self.scaredLabel.setFont(font)
        self.scaredLabel.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.scaredLabel.setObjectName("scaredLabel")
        self.verticalLayout.addWidget(self.scaredLabel)
        self.scaredBar = QProgressBar(Form)
        self.scaredBar.setMinimumSize(QSize(150, 16))
        self.scaredBar.setMaximumSize(QSize(150, 20))
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
        self.scaredBar.setObjectName("scaredBar")
        self.verticalLayout.addWidget(self.scaredBar)
        self.disgustLabel = QLabel(Form)
        self.disgustLabel.setMaximumSize(QSize(150, 32))
        font = QFont()
        font.setPointSize(16)
        self.disgustLabel.setFont(font)
        self.disgustLabel.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.disgustLabel.setObjectName("disgustLabel")
        self.verticalLayout.addWidget(self.disgustLabel)
        self.disgustBar = QProgressBar(Form)
        self.disgustBar.setMinimumSize(QSize(150, 16))
        self.disgustBar.setMaximumSize(QSize(150, 20))
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
        self.disgustBar.setObjectName("disgustBar")
        self.verticalLayout.addWidget(self.disgustBar)
        self.angryLabel = QLabel(Form)
        self.angryLabel.setMaximumSize(QSize(150, 32))
        font = QFont()
        font.setPointSize(16)
        self.angryLabel.setFont(font)
        self.angryLabel.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.angryLabel.setObjectName("angryLabel")
        self.verticalLayout.addWidget(self.angryLabel)
        self.angryBar = QProgressBar(Form)
        self.angryBar.setMinimumSize(QSize(150, 16))
        self.angryBar.setMaximumSize(QSize(150, 20))
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
        self.angryBar.setObjectName("angryBar")
        self.verticalLayout.addWidget(self.angryBar)
        self.resetBtn = QPushButton(Form)
        self.resetBtn.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resetBtn.sizePolicy().hasHeightForWidth())
        self.resetBtn.setSizePolicy(sizePolicy)
        self.resetBtn.setMinimumSize(QSize(150, 50))
        self.resetBtn.setMaximumSize(QSize(150, 50))
        font = QFont()
        font.setPointSize(16)
        self.resetBtn.setFont(font)
        self.resetBtn.setObjectName("resetBtn")
        self.verticalLayout.addWidget(self.resetBtn)
        self.gridLayout.addLayout(self.verticalLayout, 4, 4, 3, 1)
        self.resetBtn.clicked.connect(self.resetFace)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.backBtn.setText(_translate("Form", "🔙"))
        self.camLabel.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:24pt;\">Камера(загрузка...)</span></p></body></html>"))
        self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:24pt;\">Эмоции:</span></p></body></html>"))
        self.happyLabel.setText(_translate("Form", "Счастье"))
        self.surpriseLabel.setText(_translate("Form", "Удивление"))
        self.neutralLabel.setText(_translate("Form", "Спокойствие"))
        self.sadLabel.setText(_translate("Form", "Грусть"))
        self.scaredLabel.setText(_translate("Form", "Испуг"))
        self.disgustLabel.setText(_translate("Form", "Отвращение"))
        self.angryLabel.setText(_translate("Form", "Злость"))
        self.resetBtn.setText(_translate("Form", "Сменить лицо"))



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = TestWidget()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
