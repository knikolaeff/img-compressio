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

        # These attributes are made to avoid passing directories from method to method
        self.newImgFormat = None
        self.sourceDir = None
        self.destDir = None

        self.notOkMsg = qtw.QMessageBox()
        self.notOkMsg.setText("Something went wrong")

        self.ui.sourceBtn.clicked.connect(self.openSourceDirectory)
        self.ui.destinationBtn.clicked.connect(self.openDestDirectory)

        self.ui.proceedAllBtn.clicked.connect(self.proceedAll)

    def showDoneMessage(self):
        qtw.QMessageBox.information(self, "Success", "Done! Successfully edited images: %d")

    def openSourceDirectory(self):
        source_directory = qtw.QFileDialog.getExistingDirectory(
            self, "Choose a file", "")

        if source_directory:
            self.ui.sourceEntry.setText("{}".format(source_directory))

    def openDestDirectory(self):
        dest_directory = qtw.QFileDialog.getExistingDirectory(
            self, "Choose a file", "")

        if dest_directory:
            self.ui.destinationEntry.setText("{}".format(dest_directory))

    def getImgFormat(self):
        self.newImgFormat = self.ui.formatBox.currentText()

        if self.newImgFormat == "Original":
            self.newImgFormat = None

    # Overwrites sourceDir and destDir attributes with the ones in input fields
    def getSources(self):
        self.sourceDir = r"" + self.ui.sourceEntry.text() + "/"

        if self.ui.overwriteCheck.isChecked() is not True:
            self.destDir = r"" + self.ui.destinationEntry.text() + "/"
        else:
            self.destDir = self.sourceDir

    def compressAndSave(self, image, fext, new_file_path):
        quality = self.ui.qualitySpinbox.value()
        # PNG is a lossless format, hence requires separate algorithm
        if fext == ".png":
            image = image.convert(
                'P',
                palette=Image.ADAPTIVE,
                colors=256
            )
        image.save(new_file_path, self.newImgFormat, optimize=True, quality=quality)

    def proceedAll(self):
        self.getSources()
        self.getImgFormat()
        for file in os.listdir(self.sourceDir):
            fname, fext = os.path.splitext(file)
            # Saves image in a format, chosen in a spinbox, if the value in the spinbox != "Original"
            if self.newImgFormat is not None:
                fext = '.' + self.newImgFormat.lower()
            new_file_path = self.destDir + fname + "_compressio" + fext
            image = Image.open(self.sourceDir + file)
            if self.ui.resizeCheck.isChecked():
                pass
            if self.ui.compressCheck.isChecked():
                self.compressAndSave(image, fext, new_file_path)
            else:
                # If no checkboxes ticked, saves images in a chosen format
                image.save(new_file_path, self.newImgFormat)
        self.showDoneMessage()


if __name__ == '__main__':
    app = qtw.QApplication([])
    app.setStyle("Breeze")
    win = Main()
    win.show()
    app.exec()
