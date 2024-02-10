import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
root_dir= os.path.abspath(os.path.dirname(__file__))#根目录
class MathJaxExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        # 假设你的HTML文件与Python脚本在同一目录下
        html_file_path =root_dir +'/formula.html'

        # 加载HTML文件至QWebEngineView
        url = QUrl.fromLocalFile(html_file_path)
        self.web_view.load(url)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MathJaxExample()
    main_win.show()
    sys.exit(app.exec_())
