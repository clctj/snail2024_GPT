# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/clctj/snail2024_GPT/snail2020_xyzGPT.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Text_win(object):
    def setupUi(self, Text_win):
        Text_win.setObjectName("Text_win")
        Text_win.resize(1180, 841)
        Text_win.setMinimumSize(QtCore.QSize(0, 0))
        Text_win.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Text_win.setStyleSheet("background-image: url(:/snail/qrc/玻璃背景2.png);")
        self.listView = QtWidgets.QListView(Text_win)
        self.listView.setGeometry(QtCore.QRect(10, 10, 241, 681))
        self.listView.setStyleSheet("background-image: url(:/snail/qrc/米黄背景.png);")
        self.listView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listView.setProperty("isWrapping", False)
        self.listView.setWordWrap(False)
        self.listView.setObjectName("listView")
        self.question_Text = QtWidgets.QTextEdit(Text_win)
        self.question_Text.setGeometry(QtCore.QRect(260, 740, 651, 91))
        self.question_Text.setStyleSheet("color: rgb(0, 85, 255);")
        self.question_Text.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.question_Text.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.question_Text.setMarkdown("")
        self.question_Text.setObjectName("question_Text")
        self.Submit = QtWidgets.QPushButton(Text_win)
        self.Submit.setGeometry(QtCore.QRect(10, 770, 64, 64))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/snail/qrc/64gpt.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/snail/qrc/64gpt2.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.Submit.setIcon(icon)
        self.Submit.setIconSize(QtCore.QSize(64, 64))
        self.Submit.setCheckable(True)
        self.Submit.setObjectName("Submit")
        self.tools2 = QtWidgets.QGroupBox(Text_win)
        self.tools2.setGeometry(QtCore.QRect(920, 790, 251, 51))
        self.tools2.setObjectName("tools2")
        self.quit = QtWidgets.QPushButton(self.tools2)
        self.quit.setGeometry(QtCore.QRect(200, 0, 48, 48))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/snail/qrc/48退出.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.quit.setIcon(icon1)
        self.quit.setIconSize(QtCore.QSize(48, 48))
        self.quit.setFlat(True)
        self.quit.setObjectName("quit")
        self.save_text = QtWidgets.QPushButton(self.tools2)
        self.save_text.setGeometry(QtCore.QRect(150, 0, 48, 48))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/snail/qrc/48保存1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/snail/qrc/48保存2.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.save_text.setIcon(icon2)
        self.save_text.setIconSize(QtCore.QSize(48, 48))
        self.save_text.setCheckable(False)
        self.save_text.setFlat(True)
        self.save_text.setObjectName("save_text")
        self.clear_text = QtWidgets.QPushButton(self.tools2)
        self.clear_text.setGeometry(QtCore.QRect(100, 0, 48, 48))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/snail/qrc/48清屏1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clear_text.setIcon(icon3)
        self.clear_text.setIconSize(QtCore.QSize(48, 48))
        self.clear_text.setCheckable(False)
        self.clear_text.setFlat(True)
        self.clear_text.setObjectName("clear_text")
        self.repet = QtWidgets.QPushButton(self.tools2)
        self.repet.setGeometry(QtCore.QRect(50, 0, 48, 48))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/snail/qrc/list_loop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon4.addPixmap(QtGui.QPixmap(":/snail/qrc/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.repet.setIcon(icon4)
        self.repet.setIconSize(QtCore.QSize(32, 32))
        self.repet.setCheckable(True)
        self.repet.setObjectName("repet")
        self.set_gpt = QtWidgets.QPushButton(self.tools2)
        self.set_gpt.setGeometry(QtCore.QRect(0, 0, 48, 48))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/snail/qrc/32系统设置.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.set_gpt.setIcon(icon5)
        self.set_gpt.setIconSize(QtCore.QSize(32, 32))
        self.set_gpt.setCheckable(False)
        self.set_gpt.setObjectName("set_gpt")
        self.label = QtWidgets.QLabel(Text_win)
        self.label.setGeometry(QtCore.QRect(0, 700, 1171, 141))
        self.label.setStyleSheet("background-image: url(:/snail/qrc/hb3.jpg);")
        self.label.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.clear_quest = QtWidgets.QPushButton(Text_win)
        self.clear_quest.setGeometry(QtCore.QRect(860, 800, 32, 32))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/snail/qrc/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clear_quest.setIcon(icon6)
        self.clear_quest.setIconSize(QtCore.QSize(24, 24))
        self.clear_quest.setFlat(True)
        self.clear_quest.setObjectName("clear_quest")
        self.qianwen_b = QtWidgets.QCheckBox(Text_win)
        self.qianwen_b.setGeometry(QtCore.QRect(90, 710, 71, 31))
        self.qianwen_b.setObjectName("qianwen_b")
        self.buttonGroup = QtWidgets.QButtonGroup(Text_win)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.qianwen_b)
        self.xinhuo_b = QtWidgets.QCheckBox(Text_win)
        self.xinhuo_b.setGeometry(QtCore.QRect(10, 710, 71, 31))
        self.xinhuo_b.setChecked(True)
        self.xinhuo_b.setObjectName("xinhuo_b")
        self.buttonGroup.addButton(self.xinhuo_b)
        self.wenxin_b = QtWidgets.QCheckBox(Text_win)
        self.wenxin_b.setGeometry(QtCore.QRect(170, 710, 71, 31))
        self.wenxin_b.setObjectName("wenxin_b")
        self.buttonGroup.addButton(self.wenxin_b)
        self.answer_Text = QtWebEngineWidgets.QWebEngineView(Text_win)
        self.answer_Text.setGeometry(QtCore.QRect(260, 10, 911, 681))
        self.answer_Text.setStyleSheet("background-color: rgb(235, 241, 225);")
        self.answer_Text.setObjectName("answer_Text")
        self.role_list = QtWidgets.QComboBox(Text_win)
        self.role_list.setGeometry(QtCore.QRect(920, 740, 241, 32))
        self.role_list.setObjectName("role_list")
        self.role_list.addItem("")
        self.role_list.addItem("")
        self.role_list.addItem("")
        self.role_list.addItem("")
        self.role_list.addItem("")
        self.role_list.addItem("")
        self.label.raise_()
        self.question_Text.raise_()
        self.listView.raise_()
        self.Submit.raise_()
        self.tools2.raise_()
        self.clear_quest.raise_()
        self.qianwen_b.raise_()
        self.xinhuo_b.raise_()
        self.wenxin_b.raise_()
        self.answer_Text.raise_()
        self.role_list.raise_()

        self.retranslateUi(Text_win)
        QtCore.QMetaObject.connectSlotsByName(Text_win)

    def retranslateUi(self, Text_win):
        _translate = QtCore.QCoreApplication.translate
        Text_win.setWindowTitle(_translate("Text_win", "Form"))
        self.qianwen_b.setText(_translate("Text_win", "阿里"))
        self.xinhuo_b.setText(_translate("Text_win", "讯飞"))
        self.wenxin_b.setText(_translate("Text_win", "百度"))
        self.role_list.setItemText(0, _translate("Text_win", "因式分解"))
        self.role_list.setItemText(1, _translate("Text_win", "解方程根"))
        self.role_list.setItemText(2, _translate("Text_win", "几何证明"))
        self.role_list.setItemText(3, _translate("Text_win", "尺规作图"))
        self.role_list.setItemText(4, _translate("Text_win", "化学老师"))
        self.role_list.setItemText(5, _translate("Text_win", "物理老师"))

from PyQt5 import QtWebEngineWidgets
import qxjyclass_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Text_win = QtWidgets.QWidget()
    ui = Ui_Text_win()
    ui.setupUi(Text_win)
    Text_win.show()
    sys.exit(app.exec_())

