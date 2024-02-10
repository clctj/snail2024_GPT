# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/clctj/snail2024_GPT/time_date.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(563, 415)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(190, 350, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.dateEdit = QtWidgets.QDateEdit(Dialog)
        self.dateEdit.setGeometry(QtCore.QRect(50, 50, 228, 45))
        self.dateEdit.setObjectName("dateEdit")
        self.timeEdit = QtWidgets.QTimeEdit(Dialog)
        self.timeEdit.setGeometry(QtCore.QRect(50, 150, 215, 45))
        self.timeEdit.setObjectName("timeEdit")
        self.lcdNumber = QtWidgets.QLCDNumber(Dialog)
        self.lcdNumber.setGeometry(QtCore.QRect(50, 210, 191, 51))
        self.lcdNumber.setObjectName("lcdNumber")
        self.horizontalSlider = QtWidgets.QSlider(Dialog)
        self.horizontalSlider.setGeometry(QtCore.QRect(70, 300, 160, 32))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(340, 60, 117, 31))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/time/qrc/gpt_boy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.checkBox.setIcon(icon)
        self.checkBox.setIconSize(QtCore.QSize(32, 32))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.buttonGroup = QtWidgets.QButtonGroup(Dialog)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_2.setGeometry(QtCore.QRect(340, 110, 117, 31))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/time/qrc/gpt_man.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.checkBox_2.setIcon(icon1)
        self.checkBox_2.setIconSize(QtCore.QSize(32, 32))
        self.checkBox_2.setObjectName("checkBox_2")
        self.buttonGroup.addButton(self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_3.setGeometry(QtCore.QRect(340, 160, 117, 31))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/time/qrc/woman.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.checkBox_3.setIcon(icon2)
        self.checkBox_3.setIconSize(QtCore.QSize(32, 32))
        self.checkBox_3.setObjectName("checkBox_3")
        self.buttonGroup.addButton(self.checkBox_3)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(270, 350, 71, 39))
        self.pushButton.setCheckable(True)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.horizontalSlider.sliderMoved['int'].connect(self.lcdNumber.display)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "test"))

import time_rc
