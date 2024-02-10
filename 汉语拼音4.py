import sys, re
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
        self.original = self.input_text.toPlainText().replace('\n', '')  # 先移除原始文本中的换行符
        # 对原始文本进行分段处理
        chinese_paragraphs = re.split(r'[，。；？]', self.original)
        annotated_text = ''
        
        for paragraph in chinese_paragraphs:
            if not paragraph.strip():  # 跳过空段落
                continue
            # 计算当前段落内的所有汉字的拼音
            paragraph_pinyin = [item[0] for item in pinyin(paragraph, style=Style.TONE)]
            paragraph_chars = list(paragraph.strip())  # 去除首尾空白
            
            print(paragraph_chars, len(paragraph_chars),paragraph_pinyin,  len(paragraph_pinyin))
            #assert len(paragraph) == len(paragraph_pinyin), "段落内汉字列表长度与拼音列表长度不一致"
            annotated_paragraph = ''
            annotated_pinyin_paragraph = ''
            for char, pinyin_char in zip(paragraph_chars, paragraph_pinyin):
                space_count = len(pinyin_char)  # 获取当前汉字对应的拼音长度作为空格数
                spaces = ' ' * space_count
                annotated_paragraph += f"{char}{spaces}"
                annotated_pinyin_paragraph += f"{pinyin_char} "
            # 每个段落后换行
            annotated_text += annotated_pinyin_paragraph + '\n' + annotated_paragraph + '\n'
        # 更新QPlainTextEdit以展示拼音及调整后的文本
        self.input_text.setPlainText(annotated_text)
    def restore_original_text(self):
            self.input_text.setPlainText(self.original_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    annotator = PinyinAnnotator()
    annotator.show()

    sys.exit(app.exec_())
# 注意：这里仅处理了逗号分隔的情况，若要同时处理句号，请在split时加入正则表达式
# 若要考虑句号（。）分隔，则可以改为：
# chinese_sentences = re.split(r'[，。]', self.original_text)  # 根据逗号和句号划分句子
