import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView


# MathJax CDN地址
MATHJAX_CDN = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js"

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        # 加载包含MathJax引用和化学公式的HTML页面
        MATHJAX_CDN = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js"
        html_content = """
        <!-- 其他HTML头部内容 -->
        <script src="{MATHJAX_CDN}"></script>
        <!-- MathJax配置部分 -->
        <script>
          MathJax = {
            tex: {packages: ['mhchem']},
            options: {
              processHtmlClass: 'mathjax',
            },
          };
        </script>
        <!-- 正文 -->
        <p>以下是铁与氧气反应生成四氧化三铁的方程式：</p>
        <p class="mathjax">$$\ce{3Fe + 2O2 ->[\Delta] Fe3O4}$$</p>
        """

        self.web_view.setHtml(html_content)
        self.web_view.loadFinished.connect(self.on_load_finished)

    def on_load_finished(self, ok):
        if ok:
            pass
            # 确保MathJax完成渲染后调整视图大小
            # （在实际应用中可能不需要这个，MathJax通常会自动处理）
            #QTimer.singleShot(500, lambda: self.web_view.page().setZoomFactor(1))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
