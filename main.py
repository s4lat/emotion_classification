from imutils.video import VideoStream, FPS
from widgets.menuWidget import MenuWidget
from widgets.testWidget import TestWidget
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from functools import partial
from keras.models import load_model
import cfg, cv2, dlib

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.central_widget = QStackedWidget()
		self.setObjectName("centralWidget")
		self.setCentralWidget(self.central_widget)

		emotion_model_path = "static/%s" % cfg.MODELS[cfg.CURR_MODEL]
		self.emotion_classifier = load_model(emotion_model_path, compile=False)
		self.emotion_classifier._make_predict_function()

		self.face_detector = cv2.CascadeClassifier('static/haarcascade_frontalface_default.xml')

		self.menu_widget = MenuWidget(self)
		self.central_widget.addWidget(self.menu_widget)

		self.menu_widget.testBtn.clicked.connect(self.testWidget)
		self.menu_widget.exitBtn.clicked.connect(self.close)

	def testWidget(self):
		test_widget = TestWidget(cfg, face_detector=self.face_detector, 
			emotion_classifier=self.emotion_classifier, parent=self)

		self.central_widget.addWidget(test_widget)
		self.central_widget.setCurrentWidget(test_widget)
		test_widget.backBtn.clicked.connect(partial(self.backToMenu, widget=test_widget))

	def backToMenu(self, widget):
		self.central_widget.setCurrentWidget(self.menu_widget)
		widget.close()




