# 导入必要的模块
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QDate, QTime,Qt
import sys
# 引入您的Ui_Dialog类
from time_date import Ui_Dialog  # 

class MainWindow(QDialog,Ui_Dialog):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 初始化UI
       
        self.setupUi(self)

        # 设置默认日期和时间（可选）
        self.dateEdit.setDate(QDate.currentDate())
        self.timeEdit.setTime(QTime.currentTime())
        self.checkBox.stateChanged.connect(self.on_checkBox_changed)
        self.checkBox_2.stateChanged.connect(self.on_checkBox_2_changed)
        self.checkBox_3.stateChanged.connect(self.on_checkBox_3_changed)

    # 槽函数定义
    def on_checkBox_changed(self, state):
        if state == Qt.Checked:
            print("checkBox is checked")
        else:
            print("checkBox is unchecked")

    def on_checkBox_2_changed(self, state):
        if state == Qt.Checked:
            print("checkBox_2 is checked")
        else:
            print("checkBox_2 is unchecked")

    def on_checkBox_3_changed(self, state):
        if state == Qt.Checked:
            print("checkBox_3 is checked")
        else:
            print("checkBox_3 is unchecked")
    def on_pushButton_clicked(self):
        pass  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    app.exec_()