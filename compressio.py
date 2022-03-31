import sys
import os
from PyQt5 import QtWidgets as qtw
from compressio_gui import Ui_Form


class Main(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.sourceBtn.clicked.connect(self.openDirectory)

        self.setWindowTitle("Compressio")

        # self.ui.magicButton.clicked.connect(self)

    def openDirectory(self):
        directory = qtw.QFileDialog.getExistingDirectory(self, "Choose a file", "")
        if directory:
            self.ui.sourceEntry.setText("{}".format(directory))

    # def compressAll(self):


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyle("Breeze")
    win = Main()
    win.show()
    app.exec()
