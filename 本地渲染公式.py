import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
root_dir= os.path.abspath(os.path.dirname(__file__))#根目录
mathjax_path="http://127.0.0.1:8000/tex-svg.js" 
print(mathjax_path)
class MathJaxExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)
        # 创建包含MathJax引用和公式的HTML字符串
        html_content ="""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>MathJax Example</title>
            <script  type="text/javascript" id="MathJax-script" async
                src="http://127.0.0.1:8000/tex-svg.js">
            </script>
            <script type="text/x-mathjax-config">
                MathJax.Hub.Config({
                    tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]},
                    TeX: {extensions: ["AMSmath.js", "AMSsymbols.js"]},
                    CommonHTML: {scale: 100}
                });
            </script>
        </head>
        <body>
        
        <!-- 测试数学公式 -->
        <p>当 \( a \ne 0 \) 时，一元二次方程 \( ax^2 + bx + c = 0 \) 的解为：</p>
        <p>\[ x = {-b \pm \sqrt{b^2-4ac} \over 2a} \]</p>
      
        </body>
        </html>
        """
        self.web_view.setHtml(html_content)
       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MathJaxExample()
    main_win.show()
    sys.exit(app.exec_())
