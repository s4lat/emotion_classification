# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'templates_ui/quizWidget.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import os

class QuizWidget(QWidget):
    def __init__(self, cfg, parent=None):
        super(QuizWidget, self).__init__(parent)

        self.cfg = cfg

        self.good = 0
        self.bad = 0

        self.labels, self.images = self.load_images()

        self.ind = 0
        self.correct = None

        self.setupUi(self)
        self.last_setup_ui()
        self.drawImage()

    def nextImage(self, *args):
        if self.correct == None:
            return

        if self.ind == len(self.labels) - 1:
            self.ind = 0
            self.labels, self.images = self.load_images()
        else:
            self.ind += 1

        self.correct = None
        self.drawImage()
        self.updateLabels()

    def checkAnswer(self, btn):
        if self.cfg.BUTTON_TO_EMOTION[btn.objectName()] == self.labels[self.ind]:
            self.correct = True
            self.good += 1
            self.drawImage()
        else:
            self.correct = False
            self.bad += 1
            self.drawImage()

        self.updateLabels(self.cfg.BUTTON_TO_EMOTION[btn.objectName()])

    def updateLabels(self, emotion=None):
        if emotion:
            if self.correct:
                self.qLabel.setText(self.cfg.TOP_GOOD_LABEL % self.cfg.EMOTIONS_RUS[emotion])
            else:
                self.qLabel.setText(self.cfg.TOP_BAD_LABEL % 
                    (self.cfg.EMOTIONS_RUS[emotion].lower(), 
                    self.cfg.EMOTIONS_RUS[self.labels[self.ind]].lower()))
        else:
            self.qLabel.setText(self.cfg.TOP_NEUTRAL_LABEL)

        self.scoreLabel.setText(self.cfg.QUIZ_SCORE_LABEL % (self.good, self.bad, self.good+self.bad))

        # self.qLabel.adjustSize() if label not refreshing

    def drawImage(self):
        self.imgLabel.setPixmap(QPixmap(self.cfg.QUIZ_IMAGES_PATH + self.images[self.ind]))
        self.imgLabel.update()

    def load_images(self):
        images = os.listdir(self.cfg.QUIZ_IMAGES_PATH)
        images = [i for i in images if not i.startswith('.')]

        np.random.shuffle(images)

        labels = []

        for i, image in enumerate(images):
            try:
                if '%' in image:
                    label = int(image.split("%")[-1].split('.')[0])
                    if 0 <= label <= 6:
                        labels.append(label)
                        continue

                raise ValueError

            except ValueError:
                images[i] = None

        images = [img for img in images if img]

        return labels, images

    def last_setup_ui(self):
        self.imgLabel.setScaledContents(True)
        self.emotionBtns.buttonClicked.connect(self.checkAnswer)
        self.imgLabel.mousePressEvent = self.nextImage

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(925, 530)
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
        self.gridLayout.addWidget(self.backBtn, 0, 0, 1, 1)
        self.scoreLabel = QLabel(Form)
        self.scoreLabel.setStyleSheet("border: 2px solid gray;\n"
"background: rgb(240, 240, 240)")
        self.scoreLabel.setAlignment(Qt.AlignCenter)
        self.scoreLabel.setObjectName("scoreLabel")
        self.gridLayout.addWidget(self.scoreLabel, 1, 0, 1, 1)
        self.surprisedBtn = QPushButton(Form)
        self.surprisedBtn.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.surprisedBtn.sizePolicy().hasHeightForWidth())
        self.surprisedBtn.setSizePolicy(sizePolicy)
        self.surprisedBtn.setMinimumSize(QSize(150, 50))
        self.surprisedBtn.setMaximumSize(QSize(16777215, 64))
        font = QFont()
        font.setPointSize(16)
        self.surprisedBtn.setFont(font)
        self.surprisedBtn.setObjectName("surprisedBtn")
        self.emotionBtns = QButtonGroup(Form)
        self.emotionBtns.setObjectName("emotionBtns")
        self.emotionBtns.addButton(self.surprisedBtn)
        self.gridLayout.addWidget(self.surprisedBtn, 2, 2, 1, 1)
        self.neutralBtn = QPushButton(Form)
        self.neutralBtn.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.neutralBtn.sizePolicy().hasHeightForWidth())
        self.neutralBtn.setSizePolicy(sizePolicy)
        self.neutralBtn.setMinimumSize(QSize(150, 50))
        self.neutralBtn.setMaximumSize(QSize(16777215, 64))
        font = QFont()
        font.setPointSize(16)
        self.neutralBtn.setFont(font)
        self.neutralBtn.setObjectName("neutralBtn")
        self.emotionBtns.addButton(self.neutralBtn)
        self.gridLayout.addWidget(self.neutralBtn, 6, 2, 1, 1)
        self.imgLabel = QLabel(Form)
        self.imgLabel.setStyleSheet("border: 2px solid gray;\n"
"background: rgb(240, 240, 240)")
        self.imgLabel.setText("")
        self.imgLabel.setObjectName("imgLabel")
        self.gridLayout.addWidget(self.imgLabel, 1, 1, 1, 3)
        self.qLabel = QLabel(Form)
        self.qLabel.setMaximumSize(QSize(16777215, 64))
        self.qLabel.setStyleSheet("border: 2px solid gray;\n"
"background: rgb(240, 240, 240)")
        self.qLabel.setAlignment(Qt.AlignCenter)
        self.qLabel.setObjectName("qLabel")
        self.gridLayout.addWidget(self.qLabel, 0, 1, 1, 3)
        self.sadBtn = QPushButton(Form)
        self.sadBtn.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sadBtn.sizePolicy().hasHeightForWidth())
        self.sadBtn.setSizePolicy(sizePolicy)
        self.sadBtn.setMinimumSize(QSize(150, 50))
        self.sadBtn.setMaximumSize(QSize(16777215, 64))
        font = QFont()
        font.setPointSize(16)
        self.sadBtn.setFont(font)
        self.sadBtn.setObjectName("sadBtn")
        self.emotionBtns.addButton(self.sadBtn)
        self.gridLayout.addWidget(self.sadBtn, 2, 3, 1, 1)
        self.disgustBtn = QPushButton(Form)
        self.disgustBtn.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.disgustBtn.sizePolicy().hasHeightForWidth())
        self.disgustBtn.setSizePolicy(sizePolicy)
        self.disgustBtn.setMinimumSize(QSize(150, 50))
        self.disgustBtn.setMaximumSize(QSize(16777215, 64))
        font = QFont()
        font.setPointSize(16)
        self.disgustBtn.setFont(font)
        self.disgustBtn.setObjectName("disgustBtn")
        self.emotionBtns.addButton(self.disgustBtn)
        self.gridLayout.addWidget(self.disgustBtn, 5, 2, 1, 1)
        self.scaredBtn = QPushButton(Form)
        self.scaredBtn.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scaredBtn.sizePolicy().hasHeightForWidth())
        self.scaredBtn.setSizePolicy(sizePolicy)
        self.scaredBtn.setMinimumSize(QSize(150, 50))
        self.scaredBtn.setMaximumSize(QSize(16777215, 64))
        font = QFont()
        font.setPointSize(16)
        self.scaredBtn.setFont(font)
        self.scaredBtn.setObjectName("scaredBtn")
        self.emotionBtns.addButton(self.scaredBtn)
        self.gridLayout.addWidget(self.scaredBtn, 5, 1, 1, 1)
        self.happyBtn = QPushButton(Form)
        self.happyBtn.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.happyBtn.sizePolicy().hasHeightForWidth())
        self.happyBtn.setSizePolicy(sizePolicy)
        self.happyBtn.setMinimumSize(QSize(150, 50))
        self.happyBtn.setMaximumSize(QSize(16777215, 64))
        font = QFont()
        font.setPointSize(16)
        self.happyBtn.setFont(font)
        self.happyBtn.setObjectName("happyBtn")
        self.emotionBtns.addButton(self.happyBtn)
        self.gridLayout.addWidget(self.happyBtn, 2, 1, 1, 1)
        self.angryBtn = QPushButton(Form)
        self.angryBtn.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.angryBtn.sizePolicy().hasHeightForWidth())
        self.angryBtn.setSizePolicy(sizePolicy)
        self.angryBtn.setMinimumSize(QSize(150, 50))
        self.angryBtn.setMaximumSize(QSize(16777215, 64))
        font = QFont()
        font.setPointSize(16)
        self.angryBtn.setFont(font)
        self.angryBtn.setObjectName("angryBtn")
        self.emotionBtns.addButton(self.angryBtn)
        self.gridLayout.addWidget(self.angryBtn, 5, 3, 1, 1)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.disgustBtn.setText(_translate("Form", "🤢Отвращение"))
        self.qLabel.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Какую эмоцию выражает лицо на изображении?</span></p></body></html>"))
        self.scaredBtn.setText(_translate("Form", "😱Испуг"))
        self.angryBtn.setText(_translate("Form", "😡Злость"))
        self.backBtn.setText(_translate("Form", "🔙"))
        self.sadBtn.setText(_translate("Form", "😔Грусть"))
        self.surprisedBtn.setText(_translate("Form", "😯Удивление"))
        self.happyBtn.setText(_translate("Form", "😄Счастье"))
        self.neutralBtn.setText(_translate("Form", "😐Спокойствие"))
        self.scoreLabel.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:28pt; color:#00dc00; vertical-align:sub;\">✓:0</span></p><p align=\"center\"><span style=\" font-size:28pt; color:#ff0000; vertical-align:sub;\">✗:0</span></p><p align=\"center\"><span style=\" font-size:28pt; color:#000000; vertical-align:sub;\">O:0</span></p></body></html>"))




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = QuizWidget()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
