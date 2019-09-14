# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'templates_ui/testWidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(854, 577)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(854, 577))
        Form.setMaximumSize(QtCore.QSize(854, 577))
        Form.setLayoutDirection(QtCore.Qt.LeftToRight)
        Form.setAutoFillBackground(False)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(12, 12, 12, 100)
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.backBtn = QtWidgets.QPushButton(Form)
        self.backBtn.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backBtn.sizePolicy().hasHeightForWidth())
        self.backBtn.setSizePolicy(sizePolicy)
        self.backBtn.setMinimumSize(QtCore.QSize(48, 48))
        self.backBtn.setMaximumSize(QtCore.QSize(48, 48))
        font = QtGui.QFont()
        font.setPointSize(32)
        self.backBtn.setFont(font)
        self.backBtn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.backBtn.setStyleSheet("")
        self.backBtn.setObjectName("backBtn")
        self.horizontalLayout_2.addWidget(self.backBtn)
        self.camLabel = QtWidgets.QLabel(Form)
        self.camLabel.setMinimumSize(QtCore.QSize(0, 43))
        self.camLabel.setMaximumSize(QtCore.QSize(16777215, 43))
        self.camLabel.setStyleSheet("border: 2px solid gray;\n"
"")
        self.camLabel.setObjectName("camLabel")
        self.horizontalLayout_2.addWidget(self.camLabel)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 3, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.camForm = QtWidgets.QWidget(Form)
        self.camForm.setMinimumSize(QtCore.QSize(640, 360))
        self.camForm.setMaximumSize(QtCore.QSize(640, 360))
        self.camForm.setStyleSheet("border: 2px solid gray")
        self.camForm.setObjectName("camForm")
        self.gridLayout.addWidget(self.camForm, 4, 3, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 0, 10, 0)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.happyLabel = QtWidgets.QLabel(Form)
        self.happyLabel.setMaximumSize(QtCore.QSize(150, 32))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.happyLabel.setFont(font)
        self.happyLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.happyLabel.setObjectName("happyLabel")
        self.verticalLayout.addWidget(self.happyLabel)
        self.happyBar = QtWidgets.QProgressBar(Form)
        self.happyBar.setMinimumSize(QtCore.QSize(150, 16))
        self.happyBar.setMaximumSize(QtCore.QSize(150, 20))
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
        self.surpriseLabel = QtWidgets.QLabel(Form)
        self.surpriseLabel.setMaximumSize(QtCore.QSize(150, 32))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.surpriseLabel.setFont(font)
        self.surpriseLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.surpriseLabel.setObjectName("surpriseLabel")
        self.verticalLayout.addWidget(self.surpriseLabel)
        self.surpriseBar = QtWidgets.QProgressBar(Form)
        self.surpriseBar.setMinimumSize(QtCore.QSize(150, 16))
        self.surpriseBar.setMaximumSize(QtCore.QSize(150, 20))
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
        self.neutralLabel = QtWidgets.QLabel(Form)
        self.neutralLabel.setMaximumSize(QtCore.QSize(150, 32))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.neutralLabel.setFont(font)
        self.neutralLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.neutralLabel.setObjectName("neutralLabel")
        self.verticalLayout.addWidget(self.neutralLabel)
        self.neutralBar = QtWidgets.QProgressBar(Form)
        self.neutralBar.setMinimumSize(QtCore.QSize(150, 16))
        self.neutralBar.setMaximumSize(QtCore.QSize(150, 20))
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
        self.sadLabel = QtWidgets.QLabel(Form)
        self.sadLabel.setMaximumSize(QtCore.QSize(150, 32))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.sadLabel.setFont(font)
        self.sadLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.sadLabel.setObjectName("sadLabel")
        self.verticalLayout.addWidget(self.sadLabel)
        self.sadBar = QtWidgets.QProgressBar(Form)
        self.sadBar.setMinimumSize(QtCore.QSize(150, 16))
        self.sadBar.setMaximumSize(QtCore.QSize(150, 20))
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
        self.scaredLabel = QtWidgets.QLabel(Form)
        self.scaredLabel.setMaximumSize(QtCore.QSize(150, 32))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.scaredLabel.setFont(font)
        self.scaredLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.scaredLabel.setObjectName("scaredLabel")
        self.verticalLayout.addWidget(self.scaredLabel)
        self.scaredBar = QtWidgets.QProgressBar(Form)
        self.scaredBar.setMinimumSize(QtCore.QSize(150, 16))
        self.scaredBar.setMaximumSize(QtCore.QSize(150, 20))
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
        self.disgustLabel = QtWidgets.QLabel(Form)
        self.disgustLabel.setMaximumSize(QtCore.QSize(150, 32))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.disgustLabel.setFont(font)
        self.disgustLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.disgustLabel.setObjectName("disgustLabel")
        self.verticalLayout.addWidget(self.disgustLabel)
        self.disgustBar = QtWidgets.QProgressBar(Form)
        self.disgustBar.setMinimumSize(QtCore.QSize(150, 16))
        self.disgustBar.setMaximumSize(QtCore.QSize(150, 20))
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
        self.angryLabel = QtWidgets.QLabel(Form)
        self.angryLabel.setMaximumSize(QtCore.QSize(150, 32))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.angryLabel.setFont(font)
        self.angryLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.angryLabel.setObjectName("angryLabel")
        self.verticalLayout.addWidget(self.angryLabel)
        self.angryBar = QtWidgets.QProgressBar(Form)
        self.angryBar.setMinimumSize(QtCore.QSize(150, 16))
        self.angryBar.setMaximumSize(QtCore.QSize(150, 20))
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
        self.gridLayout.addLayout(self.verticalLayout, 4, 4, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
