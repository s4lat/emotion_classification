# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/aboutDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial

class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label = QtWidgets.QLabel()
        self.label.setObjectName("label")
        self.label.linkActivated.connect(partial(QtGui.QDesktopServices.openUrl, 
                            QtCore.QUrl("https://github.com/s4lat/emotion_classification")))
        self.verticalLayout_2.addWidget(self.label)

        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.okBtn = QtWidgets.QPushButton(Dialog)
        self.okBtn.setMaximumSize(QtCore.QSize(128, 16777215))
        self.okBtn.setFocusPolicy(QtCore.Qt.TabFocus)
        self.okBtn.setCheckable(False)
        self.okBtn.setAutoDefault(False)
        self.okBtn.setDefault(True)
        self.okBtn.setFlat(False)
        self.okBtn.setObjectName("okBtn")
        self.gridLayout_3.addWidget(self.okBtn, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)

        self.header = QtWidgets.QLabel(Dialog)
        self.header.setObjectName("header")
        header_pixmap = QtGui.QPixmap("assets/header_nobg.png")
        header_pixmap = header_pixmap.scaled(400, 200)
        self.header.setPixmap(header_pixmap)

        self.gridLayout.addWidget(self.header, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.okBtn.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", '<html><head/><body><p><span style=" font-size:18pt;">Название: EmoTrainer</span></p><p><span style=" font-size:18pt;">Разработчики: команда UknikiUkniki</span></p><p><span style=" font-size:18pt;">Git-репозиторий:</span><a href="https://github.com/s4lat/emotion_classification"><span style=" font-size:18pt; text-decoration: underline; color:#0000ff;"> Ссылка</span></a></p><p><span style=" font-size:18pt;"><br/></span></p></body></html>'))
        
        self.okBtn.setText(_translate("Dialog", "Ок"))
        


