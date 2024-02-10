from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

# 创建一个简单的HTML字符串，其中包含MathJax配置和LaTeX公式
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{font-size: 2em;}}
    </style>
    <script type="text/javascript" id="MathJax-script" async
      src="/mathjax/es5/tex-svg.js" id="MathJax-script" async>
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            MathJax = {{
                tex: {{
                    inlineMath: [['$', '$'], ['\\(', '\\)']]
                }}
            }};

            // 初始化MathJax并开始渲染数学公式
            MathJax.startup.promise.then(() => {{
                MathJax.typeset();
            }});
        }});
    </script>
</head>
<body>
    当你在QTextBrowser中看到这个公式：\( sin^2(x) + cos^2(x) = 1 \)，说明MathJax已成功渲染。
</body>
</html>
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        # 设置网页内容
        self.web_view.setHtml(html_content)
        #print(html_content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
