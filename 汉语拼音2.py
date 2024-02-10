from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from pypinyin import pinyin, Style
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
class PinyinAnnotatedWidget(QWidget):
    def __init__(self, chinese_text, font_size=16, spacing=5):
        super().__init__()

        self.hanzi_pinyin_dict = self.chinese_to_pinyin_dict(chinese_text)
        layout = QHBoxLayout(self)

        for hanzi, pyin in self.hanzi_pinyin_dict.items():
            # 创建垂直布局用于容纳汉字和对应的拼音标签
            vertical_layout = QVBoxLayout()

            # 创建并设置汉字标签和拼音标签样式
            hanzi_label = QLabel(hanzi)
            pinyin_label = QLabel(pyin)
            font = QFont('宋体', font_size)  # 示例：使用默认字体和字号
            hanzi_label.setFont(font)
            pinyin_label.setFont(font)
            pinyin_label.setAlignment(Qt.AlignCenter)

            # 添加到垂直布局，并保持汉字标签在下，拼音标签在上
            vertical_layout.addWidget(pinyin_label)
            vertical_layout.addSpacing(spacing)
            vertical_layout.addWidget(hanzi_label)

            # 将垂直布局添加到主水平布局中
            layout.addLayout(vertical_layout)
            layout.addSpacing(spacing)

    @staticmethod
    def chinese_to_pinyin_dict(chinese_text):
        pinyin_dict = {}
        for char in chinese_text:
            # 取第一个读音（可按需调整为多音字所有读音）
            pinyin_list = pinyin(char, style=Style.TONE)
            if pinyin_list:
                pinyin_dict[char] = pinyin_list[0][0]
                print(pinyin_dict)
        return pinyin_dict

if __name__ == "__main__":
    app = QApplication([])

    chinese_text = "你好世界，世界由我而美丽！"
    window = PinyinAnnotatedWidget(chinese_text, font_size=16, spacing=5)
    window.show()

    app.exec_()
