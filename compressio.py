import sys

from PyQt5 import QtWidgets as qtw

from compressio_prototype import Ui_Form


class Main(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.sourceBrowse.clicked.connect(self.openFileDialog)

    def openFileDialog(self):
        filename = qtw.QFileDialog.getExistingDirectory(self, "Choose a file", "")
        if filename:
            self.ui.sourcefield.setText(filename[0])


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyle("Breeze")
    win = Main()
    win.show()
    app.exec()
