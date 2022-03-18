from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Compress.io')

        self.outerLayout = qtw.QVBoxLayout()

        self.setLayout(self.outerLayout)
        self.initUI()
        self.show()

    def initUI(self):
        fileLayout = qtw.QHBoxLayout()

        controlsLayout = qtw.QGridLayout()

        self.outerLayout.addLayout(fileLayout)
        self.outerLayout.addLayout(controlsLayout)

        self.fileField = qtw.QLineEdit()

        browseBtn = qtw.QPushButton("Browse")
        browseBtn.clicked.connect(self.openFileDialog)

        fileLayout.addWidget(self.fileField)
        fileLayout.addWidget(browseBtn)

        compressBtn = qtw.QRadioButton("Compress")
        resizeBtn = qtw.QRadioButton("Resize")

        controlsLayout.addWidget(compressBtn, 0, 2, 1, 1)
        controlsLayout.addWidget(resizeBtn, 0, 3, 1, 1)

        # width = qtw.QInputDialog()
        # container.layout().addWidget(width, 1, 0, 1, 2)

    def openFileDialog(self):
        fileName = qtw.QFileDialog.getOpenFileName(self, "Choose a file", "", "All files (*)")
        if fileName:
            self.fileField.setText(fileName[0])


app = qtw.QApplication([])
app.setStyle("Breeze")
win = MainWindow()
app.exec()
