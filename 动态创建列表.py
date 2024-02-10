from PyQt5.QtWidgets import QApplication, QComboBox, QVBoxLayout, QWidget
import sys
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建一个QComboBox
        self.combo_box = QComboBox(self)

        # 增加列表项
        self.combo_box.addItems(["Item 1", "Item 2", "Item 3"])

        # 创建一个垂直布局并将QComboBox添加到窗口中
        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        self.setLayout(layout)

    def add_item(self, item_text):
        """增加一个列表项"""
        self.combo_box.addItem(item_text)

    def remove_item(self, index):
        """根据索引删除一个列表项"""
        if index < self.combo_box.count():
            self.combo_box.removeItem(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    # 动态增加一个列表项
    window.add_item("Item 4")

    # 动态删除第一个列表项
    #window.remove_item(0)

    app.exec_()
