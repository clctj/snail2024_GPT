import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
import qianfan
class ChatUI(QWidget):
    def __init__(self):
        super().__init__()
        qianfan.AK("MHxGnqfX4grPAOkoaAi0w75R")
        qianfan.SK("QIteInbvmGr5PsffdG55ea5ZRG081IRY")
        self.chat_comp = qianfan.ChatCompletion()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('聊天窗口')

        # 提问框
        self.question_edit = QLineEdit(self)
        self.question_edit.setPlaceholderText("请输入你的问题")

        # 答案框（使用QTextEdit以便显示多行文本）
        self.answer_text = QTextEdit(self)
        self.answer_text.setReadOnly(True)

        # 提交按钮
        self.submit_button = QPushButton('提交', self)
        self.submit_button.clicked.connect(self.handle_submit)

        # 布局管理
        layout = QVBoxLayout()
        layout.addWidget(self.question_edit)
        layout.addWidget(self.answer_text)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def handle_submit(self):
        question = self.question_edit.text()
        msgs = qianfan.Messages()
        msgs.append(question)
     
        resp = self.chat_comp.do(messages=msgs)
        text_content = resp['body']['result']

        self.answer_text.setText(text_content)
        self.question_edit.clear()  # 清空输入框以准备下一次输入

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = ChatUI()
    ui.show()

    sys.exit(app.exec_())
