from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from markdown import markdown
from markdownify import markdownify as md  
class MainWindow(QMainWindow):  
    def __init__(self, app):  
        super().__init__()  
        self.browser = QWebEngineView()  
        self.setCentralWidget(self.browser)  
        self.browser.page().runJavaScript("""  
            window.MathJax = {  
                tex2jax: {  
                    inlineMath: [['$', '$'], ['\\(', '\\)']]  
                }  
            };  
            MathJax.Hub.Config({  
                showMathMenu: false, // 禁用菜单显示  
                messageStyle: "none" // 不显示错误信息  
            });  
            MathJax.Hub.Queue(["Typeset", MathJax.Hub, this.document]);  
        """)  
        self.loadMarkdown()  
      
    def loadMarkdown(self):  
        markdown_text = """  
        ## Markdown with MathJax Example  
        $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$  
        """  
        html = md(markdown_text)  
        self.browser.setHtml(html)
if __name__ == '__main__': 
    import sys  
    app = QApplication(sys.argv)  
    ui = MainWindow(app)  
    ui.show()  
    app.exec_()
