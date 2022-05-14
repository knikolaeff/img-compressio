import os
import threading
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
        self.setWindowIcon(QIcon(r"src/icon.ico"))

        # These attributes are made to avoid passing directories from method to method
        self.source_dir = None
        self.dest_dir = None
        self.quality = 75

        self.ui.sourceBtn.clicked.connect(self.open_source_directory)
        self.ui.destinationBtn.clicked.connect(self.open_dest_directory)

        self.ui.proceedAllBtn.clicked.connect(self.proceed_all)

    def show_done_message(self, counter):
        qtw.QMessageBox.information(
            self, "Success", f"Done! Successfully edited images: {counter}")

    def show_fail_message(self):
        qtw.QMessageBox.information(self, "Fail", "Fields cannot be empty!")

    def open_source_directory(self):
        directory = qtw.QFileDialog.getExistingDirectory(
            self, "Choose Directory", "", qtw.QFileDialog.DontUseNativeDialog)

        if directory:
            self.ui.sourceEntry.setText(directory)

    def open_dest_directory(self):
        directory = qtw.QFileDialog.getExistingDirectory(
            self, "Choose Directory", "", qtw.QFileDialog.DontUseNativeDialog)

        if directory:
            self.ui.destinationEntry.setText(directory)

    # Overwrites empty sourceDir and destDir attributes with directories from the input fields
    # If any of the fields is empty - raise an exception that will be caught
    def get_sources(self):

        if self.ui.sourceEntry.text() == "" or self.ui.destinationEntry.text() == "":
            raise ValueError("Fields cannot be empty")

    # 'r' in front of string means raw string. It will ignore escape sequences
        self.source_dir = r"" + self.ui.sourceEntry.text() + "/"

        if self.ui.overwriteCheck.isChecked():
            self.dest_dir = self.source_dir
        else:
            self.dest_dir = r"" + self.ui.destinationEntry.text() + "/"

    def resize_image(self, image):
        width = self.ui.widthSpinbox.value()
        height = self.ui.heightSpinbox.value()
        image = image.resize((width, height))
        return image

    def compress_image(self, image, fext):

        # PNG is a lossless format, hence requires separate algorithm
        if fext == ".png":
            image = image.convert(
                'P',
                palette=Image.ADAPTIVE,
                colors=256
            )

        return image

    def proceed_all(self):
        counter = 0
        progress = 0
        self.quality = self.ui.qualitySpinbox.value()

        # return keyword in the except body stops the function
        try:
            self.get_sources()
        except ValueError:
            self.show_fail_message()
            return
        # Saves image in a format, chosen in a spinbox, if the value in the spinbox != "Original"
        # if it is, format remains the same
        img_format = self.ui.formatBox.currentText().lower(
        ) if self.ui.formatBox.currentText() != "Original" else None

        extensions = (".png", ".jpg", ".jpeg", ".bmp", ".jfif")
        files = [file for file in os.listdir(
            self.source_dir) if file.endswith(extensions)]

        self.ui.progressBar.setMaximum(len(files))

        for file in files:
            self.process_file(file, img_format)

            counter += 1
            progress += 1
            self.ui.progressBar.setValue(progress)

        self.show_done_message(counter)
        self.ui.progressBar.setValue(0)

    def process_file(self, file, img_format):
        fname, fext = os.path.splitext(file)

        fext = '.' + img_format if img_format is not None else '.' + fext

        new_file_path = self.dest_dir + fname + "_compressio" + fext

        image = Image.open(self.source_dir + file)

        if self.ui.resizeCheck.isChecked():
            image = self.resize_image(image)
        if self.ui.compressCheck.isChecked():
            image = self.compress_image(image, fext)

        image.save(new_file_path, optimize=True, quality=self.quality)


if __name__ == '__main__':
    app = qtw.QApplication([])
    app.setStyle("Breeze")
    win = Main()
    win.show()
    app.exec()
