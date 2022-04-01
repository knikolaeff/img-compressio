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

        self.okMsg = qtw.QMessageBox()
        self.okMsg.setText("Done!")

        self.notOkMsg = qtw.QMessageBox()
        self.notOkMsg.setText("Something went wrong")

        self.ui.sourceBtn.clicked.connect(self.openSourceDirectory)
        self.ui.destinationBtn.clicked.connect(self.openDestDirectory)

        self.ui.compressAllBtn.clicked.connect(self.proceedAll)

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
        # try:
        sourceDir, destDir = self.getSources()
        imgFormat = self.saveAs()
        quality = self.ui.qualitySpinbox.value()
        for file in os.listdir(sourceDir):
            fname, fext = os.path.splitext(file)
            if imgFormat is not None:
                fext = imgFormat.lower()
            newFilePath = destDir + fname + "_resized" + fext
            image = Image.open(sourceDir + file)
            if fext == ".png":
                image = image.convert(
                    'P',
                    palette=Image.ADAPTIVE,
                    colors=256
                )
            image.save(newFilePath, imgFormat, optimize=True)
        self.okMsg.exec()

        # except:
        #     self.notOkMsg.exec()

    def saveAs(self):
        imgFormat = self.ui.formatBox.currentText()
        if imgFormat == "Original":
            imgFormat = None
        return imgFormat

    def getSources(self):
        sourceDir = r"" + self.ui.sourceEntry.text() + "/"
        if self.ui.overwriteCheck.isChecked() is not True:
            destDir = r"" + self.ui.destinationEntry.text() + "/"
        else:
            destDir = sourceDir
        return sourceDir, destDir

    def proceedAll(self):
        imgFormat = self.saveAs()

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
