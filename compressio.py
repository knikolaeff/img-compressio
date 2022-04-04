import sys
import os
from PIL import Image
from PyQt5 import QtWidgets as qtw
from compressio_gui import Ui_Form


class Main(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.setWindowTitle("Compressio")

        self.newImgFormat = None
        self.sourceDir = None
        self.destDir = None

        self.okMsg = qtw.QMessageBox()
        self.okMsg.setText("Done!")

        self.notOkMsg = qtw.QMessageBox()
        self.notOkMsg.setText("Something went wrong")

        self.ui.sourceBtn.clicked.connect(self.openSourceDirectory)
        self.ui.destinationBtn.clicked.connect(self.openDestDirectory)

        self.ui.proceedAllBtn.clicked.connect(self.proceedAll)

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

    def compress(self):
        self.getSources()
        self.saveAs()
        for file in os.listdir(self.sourceDir):
            fname, fext = os.path.splitext(file)
            # Saves image in a format, chosen in a spinbox, if the value in the spinbox != "Original"
            if self.newImgFormat is not None:
                fext = self.newImgFormat.lower()
            newFilePath = self.destDir + fname + "_compressio" + fext
            image = Image.open(self.sourceDir + file)
            quality = self.ui.qualitySpinbox.value()
            if fext == ".png":
                image = image.convert(
                    'P',
                    palette=Image.ADAPTIVE,
                    colors=256
                )
            image.save(newFilePath, self.newImgFormat, optimize=True, quality=quality)
        self.okMsg.exec()

    def saveAs(self):
        self.newImgFormat = self.ui.formatBox.currentText()
        if self.newImgFormat == "Original":
            self.newImgFormat = None

    def getSources(self):
        sourceDir = r"" + self.ui.sourceEntry.text() + "/"
        if self.ui.overwriteCheck.isChecked() is not True:
            destDir = r"" + self.ui.destinationEntry.text() + "/"
        else:
            destDir = sourceDir
        return sourceDir, destDir

    def proceedAll(self):

        if self.ui.compressCheck.isChecked():
            self.compress()
        elif self.ui.resizeCheck.isChecked():
            pass


if __name__ == '__main__':
    app = qtw.QApplication([])
    app.setStyle("Breeze")
    win = Main()
    win.show()
    app.exec()
