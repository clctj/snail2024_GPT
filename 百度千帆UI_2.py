import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import qianfan
class ChatWorker(QObject):
    answer_signal = pyqtSignal(str)  # 创建一个信号用于传递答案
    qianfan.AK("MHxGnqfX4grPAOkoaAi0w75R")
    qianfan.SK("QIteInbvmGr5PsffdG55ea5ZRG081IRY")

    def do_chat(self, question):
        
        chat_comp = qianfan.ChatCompletion()
        msgs = qianfan.Messages()
        msgs.append(question)
        resp = chat_comp.do(messages=msgs)
        text_content = resp['body']['result']

        self.answer_signal.emit(text_content)  # 发射信号传递答案

class ChatUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        # 初始化聊天后台工作线程
        self.chat_worker = ChatWorker()
        self.chat_worker.answer_signal.connect(self.update_answer)  # 连接信号到槽函数

    def initUI(self):
        self.setWindowTitle('聊天窗口')

        # 提问框
        self.question_edit = QLineEdit(self)
        self.question_edit.setPlaceholderText("请输入你的问题")
        self.question_edit.returnPressed.connect(self.handle_submit)  # 按下回车键即视为提交

        # 答案框（使用QTextEdit以便显示多行文本）
        self.answer_text = QTextEdit(self)
        self.answer_text.setReadOnly(True)
        
        layout = QVBoxLayout()
        layout.addWidget(self.question_edit)
        layout.addWidget(self.answer_text)
       
        self.setLayout(layout)
         # 提交按钮
        
    def handle_submit(self):
        question = self.question_edit.text()
        self.chat_worker.do_chat(question)  # 开始处理聊天任务

    def update_answer(self, text_content):
        self.answer_text.append(text_content)  # 在原有内容基础上追加新答案
        self.question_edit.clear()  # 清空输入框以准备下一次输入

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = ChatUI()
    ui.show()
    sys.exit(app.exec_())
