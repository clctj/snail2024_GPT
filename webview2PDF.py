import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QMarginsF
from PyQt5.QtGui import QPageLayout, QPageSize

app = QtWidgets.QApplication(sys.argv)
loader = QtWebEngineWidgets.QWebEngineView()
loader.load(QtCore.QUrl('http://163.com'))

layout = QPageLayout(
    QPageSize(QPageSize.A4),
    QPageLayout.Portrait, QMarginsF(0, 0, 0, 0)
)

def printFinished():
    page = loader.page()
    print("%s Printing Finished!" % page.title())
    app.exit()

def printToPDF(finished):
    loader.show()
    page = loader.page()
    page.printToPdf("pdf%s.pdf" % page.title(), layout)


loader.page().pdfPrintingFinished.connect(printFinished)
loader.loadFinished.connect(printToPDF)

app.exec_()
