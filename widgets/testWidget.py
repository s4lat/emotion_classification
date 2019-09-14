# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'templates_ui/testWidget.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!
from keras.preprocessing.image import img_to_array
from PyQt5 import QtCore, QtGui, QtWidgets
from imutils.video import VideoStream, FPS
import queue, threading, cv2
import numpy as np
from utils import *

class FrameWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FrameWidget, self).__init__(parent)
        self.parent = parent
        self.cam_frame = None

        self.mousePressEvent = self.click

    def set_frame(self, frame):
        self.cam_frame = frame
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.cam_frame:
            qp.drawImage(QtCore.QPoint(0, 0), self.cam_frame)
        qp.end()

    def click(self, event):
        coords = event.pos()
        coords = (coords.x(), coords.y())
        self.parent.chooseFace(coords)

class TestWidget(QtWidgets.QWidget):
    def __init__(self, cfg, face_detector, emotion_classifier, parent=None):
        super(TestWidget, self).__init__(parent)

        self.cfg = cfg

        self.face_detector = face_detector
        self.emotion_classifier = emotion_classifier

        self.faces = None
        self.tracker_initiated = False
        self.gray = None

        self.running = True
        self.q = queue.Queue()

        self.capture_thread = threading.Thread(target=self.grab, args = (0, self.q, self.cfg.OUT_WIDTH, self.cfg.OUT_HEIGHT))
        self.capture_thread.start()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
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



    def grab(self, cam, queue, width, height):
        try:
            input_shape = self.emotion_classifier.layers[0].input_shape[1:3]

            self.tracker_initiated = False

            cap = VideoStream(src=0).start()
            fps = FPS().start()
            frame_ind = 0
            CURRENT_FPS = 0

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
                        emotion = np.argmax(preds)

                        x, y, w, h = (x*self.cfg.SCALE_FACTOR, y*self.cfg.SCALE_FACTOR, w*self.cfg.SCALE_FACTOR, h*self.cfg.SCALE_FACTOR)
                        x, y, w, h = (int(x), int(y), int(w), int(h))

                        draw_border(out_frame, (x, y), (x+w, y+h), self.cfg.SELECTED_COLOR, 2, 5, 10)
                    else:
                        self.tracker_initiated = False

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

                    result = {'img' : out_frame}

                    queue.put(result)
        except Exception as e:
            print(e)
            
        finally:
            cap.stop()

    def update_frame(self):
        if not self.q.empty():
            frame = self.q.get()
            img = cv2.cvtColor(frame["img"], cv2.COLOR_BGR2RGB)

            height, width, bpc = img.shape
            bpl = bpc * width
            img = QtGui.QImage(img, width, height, bpl, QtGui.QImage.Format_RGB888)
            self.camForm.set_frame(img)

    def closeEvent(self, event):
        self.running = False


    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(664, 552)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.backBtn = QtWidgets.QPushButton(Form)
        self.backBtn.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backBtn.sizePolicy().hasHeightForWidth())
        self.backBtn.setSizePolicy(sizePolicy)
        self.backBtn.setMinimumSize(QtCore.QSize(50, 50))
        self.backBtn.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.backBtn.setFont(font)
        self.backBtn.setObjectName("backBtn")
        self.gridLayout.addWidget(self.backBtn, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.camForm = FrameWidget(Form)
        self.camForm.setMinimumSize(QtCore.QSize(640, 480))
        self.camForm.setMaximumSize(QtCore.QSize(640, 480))
        self.camForm.setObjectName("camForm")
        self.gridLayout.addWidget(self.camForm, 1, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.backBtn.setText(_translate("Form", "B"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = TestWidget()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
