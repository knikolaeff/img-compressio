import os
from PIL import Image
from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QIcon
from compressio_gui import Ui_Form


class Main(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.setWindowTitle("Compressio")
        self.setWindowIcon(QIcon('icon.ico'))

        # These attributes are made to avoid passing directories from method to method
        self.newImgFormat = None
        self.sourceDir = None
        self.destDir = None

        self.ui.sourceBtn.clicked.connect(self.openSourceDirectory)
        self.ui.destinationBtn.clicked.connect(self.openDestDirectory)

        self.ui.proceedAllBtn.clicked.connect(self.proceedAll)

    def showDoneMessage(self, counter):
        qtw.QMessageBox.information(
            self, "Success", "Done! Successfully edited images: {:d}".format(counter))

    def showFailMessage(self):
        qtw.QMessageBox.information(self, "Fail", "Something went wrong")

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

    # Overwrites empty sourceDir and destDir attributes with directories from the input fields
    def getSources(self):
        self.sourceDir = r"" + self.ui.sourceEntry.text() + "/"

        if self.ui.overwriteCheck.isChecked():
            self.destDir = self.sourceDir
        else:
            self.destDir = r"" + self.ui.destinationEntry.text() + "/"

    def resizeImage(self, image):
        width = self.ui.widthSpinbox.value()
        height = self.ui.heightSpinbox.value()
        image = image.resize((width, height))
        return image

    def compressImage(self, image, fext):
        quality = self.ui.qualitySpinbox.value()

        # PNG is a lossless format, hence requires separate algorithm
        if fext == ".png":
            image = image.convert(
                'P',
                palette=Image.ADAPTIVE,
                colors=256
            )

        return image, quality

    def proceedAll(self):
        counter = 0
        progress = 0

        self.getSources()
        self.getImgFormat()
        self.ui.progressBar.setMaximum(len(os.listdir(self.sourceDir)))

        extensions = (".png", ".jpg", ".jpeg", ".bmp", ".jfif")
        files = [file for file in os.listdir(
            self.sourceDir) if file.endswith(extensions)]

        for file in files:
            self.processFile(file)

            counter += 1
            progress += 1
            self.ui.progressBar.setValue(progress)

        self.showDoneMessage(counter)

    def processFile(self, file):
        fname, fext = os.path.splitext(file)

        # Saves image in a format, chosen in a spinbox, if the value in the spinbox != "Original"
        if self.newImgFormat is not None:
            fext = '.' + self.newImgFormat.lower()

        new_file_path = self.destDir + fname + "_compressio" + fext

        image = Image.open(self.sourceDir + file)

        if self.ui.resizeCheck.isChecked():
            image = self.resizeImage(image)

        if self.ui.compressCheck.isChecked():
            image, quality = self.compressImage(image, fext)

        # If no checkboxes ticked, saves images in a chosen format
        image.save(new_file_path, self.newImgFormat,
                   optimize=True, quality=quality)


if __name__ == '__main__':
    app = qtw.QApplication([])
    app.setStyle("Breeze")
    win = Main()
    win.show()
    app.exec()
