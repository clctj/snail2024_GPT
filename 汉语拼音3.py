import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QPlainTextEdit
from pypinyin import pinyin, Style

class PinyinAnnotator(QWidget):
    def __init__(self):
        super().__init__()

        self.input_text = QPlainTextEdit()
        self.annotate_button = QPushButton("标注拼音")
        self.annotate_button.clicked.connect(self.annotate_and_show_pinyin)
        self.restore_button = QPushButton("还原文字")
        self.restore_button.clicked.connect(self.restore_original_text)

        layout = QVBoxLayout()
        layout.addWidget(self.input_text)
        layout.addWidget(self.annotate_button)
        layout.addWidget(self.restore_button)

        self.setLayout(layout)
        self.original_text = ''

    def annotate_and_show_pinyin(self):
        self.original_text = self.input_text.toPlainText()
        # 计算拼音并按字符分割
        pinyin_list = [item[0] for item in pinyin(self.original_text, style=Style.TONE)]
        chinese_chars = list(self.original_text)
        annotated_text = ''
        space_counts = [len(p) for p in pinyin_list]  
        for i in range(0, len(chinese_chars), 10):  # 每次移动10个字符
            spaces = ' ' * (space_counts[i]) # 根据空格数量生成空格字符串
            current_chinese_subtext =spaces.join(chinese_chars[i:i+10])
            current_pinyin_subtext = ' '.join(pinyin_list[i:i+10])
            annotated_text += f"{current_pinyin_subtext}\n{current_chinese_subtext}\n"

        # 更新QPlainTextEdit以展示拼音
        self.input_text.setPlainText(annotated_text)

    def restore_original_text(self):
        self.input_text.setPlainText(self.original_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    annotator = PinyinAnnotator()
    annotator.show()

    sys.exit(app.exec_())
