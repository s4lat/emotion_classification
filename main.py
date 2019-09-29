from imutils.video import VideoStream, FPS
from widgets.menuWidget import MenuWidget
from widgets.detectWidget import DetectWidget
from widgets.quizWidget import QuizWidget
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from functools import partial
from keras.models import load_model
from keras import backend as K
import cfg, cv2

def swish_activation(x):
  return (K.sigmoid(x) * x)

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.central_widget = QStackedWidget()
		self.setObjectName("centralWidget")
		self.setCentralWidget(self.central_widget)
		self.setMinimumSize(1024, 640)

		emotion_model_path = cfg.MODELS[cfg.CURR_MODEL]
		self.emotion_classifier = load_model(emotion_model_path, 
			custom_objects={"swish_activation": swish_activation}, compile=False)
		self.emotion_classifier._make_predict_function()

		self.face_detector = cv2.CascadeClassifier(cfg.FRONTAL_FACE_DETECTOR)

		self.menu_widget = MenuWidget(self)
		self.central_widget.addWidget(self.menu_widget)

		self.menu_widget.quizBtn.clicked.connect(self.quizWidget)
		self.menu_widget.freeBtn.clicked.connect(self.detectWidget)
		self.menu_widget.exitBtn.clicked.connect(self.close)

	def detectWidget(self):
		detect_widget = DetectWidget(cfg, face_detector=self.face_detector, 
			emotion_classifier=self.emotion_classifier, parent=self)

		self.central_widget.addWidget(detect_widget)
		self.central_widget.setCurrentWidget(detect_widget)
		detect_widget.backBtn.clicked.connect(partial(self.backToMenu, widget=detect_widget))

	def quizWidget(self):
		quiz_widget = QuizWidget(cfg, parent=self)

		self.central_widget.addWidget(quiz_widget)
		self.central_widget.setCurrentWidget(quiz_widget)
		quiz_widget.backBtn.clicked.connect(partial(self.backToMenu, widget=quiz_widget))


	def backToMenu(self, widget):
		self.central_widget.setCurrentWidget(self.menu_widget)
		widget.close()




