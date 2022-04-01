import sys
import os
import PIL
from PyQt5 import QtWidgets as qtw
from compressio_gui import Ui_Form


class Main(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.okMsg = qtw.QMessageBox()
        self.okMsg.setText("Done!")

        self.notOkMsg = qtw.QMessageBox()
        self.notOkMsg.setText("Something went wrong")

        self.ui.sourceBtn.clicked.connect(self.openSourceDirectory)
        self.ui.destinationBtn.clicked.connect(self.openDestDirectory)
        self.ui.compressAllBtn.clicked.connect(self.compressAll)

        self.setWindowTitle("Compressio")

    def openSourceDirectory(self):
        sourceDirectory = qtw.QFileDialog.getExistingDirectory(
            self, "Choose a file", "")

        if sourceDirectory:
            self.ui.sourceEntry.setText("{}".format(sourceDirectory))

    def openDestDirectory(self):
        destDirectory = qtw.QFileDialog.getExistingDirectory(
            self, "Choose a file", "")

        if destDirectory:
            self.ui.destinationEntry.setText("{}".format(destDirectory))

    def compressAll(self, path):

        sourceDir = self.ui.sourceEntry.text()
        destDir = self.ui.destinationEntry.text()
        quality = self.ui.qualitySpinbox.value()
        imgFormat = self.ui.formatBox.currentText()
        if imgFormat == "Original":
            imgFormat = None

        try:
            for file in os.listdir(sourceDir):
                image = PIL.Image.open(path + file)
                image.save(destDir, imgFormat, optimize=True, quality=quality)
                okMsg.exec()

        except:
            self.notOkMsg.exec()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyle("Breeze")
    win = Main()
    win.show()
    app.exec()
