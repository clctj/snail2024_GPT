import sys
from PyQt5.QtWidgets import QApplication, QTextBrowser, QWidget, QVBoxLayout
import markdown2

# Markdown文本
markdown_text = "**你好** *World* [Link](https://example.com)"

# 转换为HTML
html_text = markdown2.markdown(markdown_text)

app = QApplication(sys.argv)
browser = QTextBrowser()

# 设置转换后的HTML内容
browser.setHtml(html_text)

window = QWidget()
layout = QVBoxLayout(window)
layout.addWidget(browser)

window.show()
sys.exit(app.exec_())
