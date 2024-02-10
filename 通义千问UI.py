import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QPushButton, QWidget
from dashscope import Generation
import dashscope

class GPTChatWindow(QMainWindow):
    def __init__(self):
        super(GPTChatWindow, self).__init__()
        dashscope.api_key="sk-8491f91887c846dcbeae2b8b1f5b0b32"
        
        # 创建UI组件
        self.user_input = QTextEdit(self)
        self.answer_output = QTextEdit(self, readOnly=True)
        self.submit_button = QPushButton('提交', self)

        # 设置组件属性
        self.setWindowTitle('GPT对话助手')
        self.user_input.setPlaceholderText('请输入您的问题...')
        self.answer_output.setPlaceholderText('在这里显示AI的回答...')
        self.submit_button.clicked.connect(self.handle_submit)

        # 布局管理
        layout = QVBoxLayout()
        layout.addWidget(self.user_input)
        layout.addWidget(self.answer_output)
        layout.addWidget(self.submit_button)
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # 初始化时模拟一次欢迎语（实际应用中可以保留此行以展示欢迎信息）
        self.show_answer("欢迎使用GPT对话助手！请输入您的第一个问题...")

    def call_with_messages(self, question):
        messages=[ {'role': 'user', 'content': question}]
        gen = Generation()  # 'chatglm3-6b',
        response = gen.call(
            Generation.Models.qwen_turbo,
            messages=messages,
            result_format='message'
        )
        answer = response['output']['choices'][0]['message']['content']
        return answer

    def handle_submit(self):
        user_question = self.user_input.toPlainText()
        if user_question:
            self.gpt_response = self.show_answer(user_question)
            # 保持用户输入内容，光标移动到文本末尾
            self.user_input.setText(self.user_input.toPlainText())
            #self.user_input.moveCursor(QTextCursor.End)

    def show_answer(self, question):
        self.gpt_response = self.call_with_messages(question)
        self.answer_output.append(f"\nAI: {self.gpt_response}\n")  # 追加回答而不覆盖原有内容

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GPTChatWindow()
    window.show()
    sys.exit(app.exec_())
