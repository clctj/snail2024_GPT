
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QFrame, QSizePolicy
from pypinyin import pinyin, Style
from PyQt5.QtGui import QFont, QFontMetrics

class PinyinAnnotatedWidget(QWidget):
    def __init__(self, chinese_text, font=None, font_size=12, max_chars_per_line=10, char_spacing=3):
        super().__init__()

        self.chinese_text = chinese_text
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        if font is None:
            self.font = QFont('宋体', font_size)  # 使用默认字体和字号
        else:
            self.font = font
        

        # 将汉字转为拼音
        pinyin_list = []
        for word in chinese_text:
            pinyin_word = ' '.join([item[0] for item in pinyin(word, style=Style.TONE)])
            pinyin_list.append(pinyin_word)

        current_line_hanzi = ''
        current_line_pinyin = ''
        line_width = 0

        for index, (hanzi, pinyin_str) in enumerate(zip(chinese_text, pinyin_list)):
            next_char_width = QFontMetrics(self.font).width(hanzi)
            next_pinyin_width = QFontMetrics(self.font).width(pinyin_str)
            # 计算当前字是否会导致超出最大字符数对应的宽度
            if line_width + next_char_width + next_pinyin_width + char_spacing > max_chars_per_line * QFontMetrics(self.font).averageCharWidth():
                # 创建并添加当前行的汉字和拼音标签
                self.add_line_to_layout(current_line_hanzi, current_line_pinyin, layout, char_spacing)
                current_line_hanzi = hanzi
                current_line_pinyin = pinyin_str
                line_width = next_char_width + next_pinyin_width + char_spacing
            else:
                current_line_hanzi += hanzi + ' '
                current_line_pinyin += pinyin_str + ' '
                line_width += next_char_width + next_pinyin_width + char_spacing

        # 添加最后一行（如果存在）
        if current_line_hanzi:
            self.add_line_to_layout(current_line_hanzi.strip(), current_line_pinyin.strip(), layout, char_spacing)

    def add_line_to_layout(self, chinese_line, pinyin_line, layout, char_spacing):
        # 创建汉字标签
        hanzi_label = QLabel(chinese_line, self)
        hanzi_label.setFont(self.font)
        print (pinyin_line)

        # 创建拼音标签并设置位置
        pinyin_label = QLabel(pinyin_line, self)
        pinyin_label.setFont(self.font)
        fm = QFontMetrics(self.font)
        base_pos = hanzi_label.pos()
        x_offset = base_pos.x()# + fm.horizontalAdvance(chinese_line) + char_spacing
        y_offset = base_pos.y()  # 
        pinyin_label.move(x_offset, y_offset)
        pinyin_label.setStyleSheet("color: gray;")  # 设置拼音颜色
        layout.addWidget(pinyin_label)  # 添加拼音标签到布局中
    
        layout.addWidget(hanzi_label)#添加标签
        # 添加一个水平分割线来模拟换行效果
        line_separator = QFrame()
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        separator_height = fm.height() # 分割线高度
        line_separator.setMaximumHeight(separator_height)
        layout.addWidget(line_separator)

      

# 在主程序中使用自定义字体、字号、最大字数以及汉字与拼音之间的间距
if __name__ == "__main__":
    app = QApplication([])

    custom_font = QFont("微软雅黑", 16)  # 示例：使用自定义字体和字号
    chinese_text = "你好，世界！这是一个很长的句子，用来测试分行功能。"
    window = PinyinAnnotatedWidget(chinese_text, font=custom_font, max_chars_per_line=50, char_spacing=3)
    window.show()

    app.exec_()
