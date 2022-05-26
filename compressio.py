import os
from multiprocessing.pool import ThreadPool
from PIL import Image
from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QThread, QObject
from compressio_gui import Ui_Form


class Worker(QObject):
    '''
    This class is responsible for batch imame processing itself.
    '''
    finished = pyqtSignal()
    success = pyqtSignal(int)
    error = pyqtSignal()
    progress = pyqtSignal()

    def run(self):

        # return keyword in the except body stops the function
        try:
            win.get_sources()
        except ValueError:
            self.error.emit()
            return

        win.quality = win.ui.qualitySpinbox.value()

        # Saves image in a format, chosen in a spinbox, if the value in the spinbox != "Original"
        # if it is, format remains the same
        self.img_format = win.ui.formatBox.currentText().lower(
        ) if win.ui.formatBox.currentText() != "Original" else None

        extensions = (".png", ".jpg", ".jpeg", ".bmp", ".jfif")
        files = [file for file in os.listdir(
            win.source_dir) if file.endswith(extensions)]

        win.ui.progressBar.setMaximum(len(files))

        p = ThreadPool()
        log = p.map(self.process_file, files)

        p.close()
        p.join()

        self.success.emit(len(log))
        self.finished.emit()

    def process_file(self, file):
        fname, fext = os.path.splitext(file)

        fext = '.' + self.img_format if self.img_format is not None else fext

        new_file_path = win.dest_dir + fname + "_compressio" + fext

        image = Image.open(win.source_dir + file)

        if win.ui.resizeCheck.isChecked():
            image = self.resize_image(image)
        if win.ui.compressCheck.isChecked():
            image = self.compress_image(image, fext)

        image.save(new_file_path, optimize=True, quality=win.quality)
        self.progress.emit()
        image.close()

    def resize_image(self, image):
        width = win.ui.widthSpinbox.value()
        height = win.ui.heightSpinbox.value()
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


class Main(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.setWindowTitle("Compressio")
        self.setWindowIcon(QIcon('icon.ico'))

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

    def proceed_all(self):
        '''
        Creates separate thread and instantiating Worker class in it.
        Messaboxes, progressbar and counter are updating via Qt signals.
        '''
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.nullify_progress)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.success.connect(self.show_done_message)
        self.worker.error.connect(self.show_fail_message)
        self.worker.progress.connect(self.record_progress)

        self.thread.start()

    def record_progress(self):
        value = self.ui.progressBar.value()
        self.ui.progressBar.setValue(value + 1)

    def nullify_progress(self):
        self.ui.progressBar.setValue(0)

if __name__ == '__main__':
    app = qtw.QApplication([])
    app.setStyle("Breeze")
    win = Main()
    win.show()
    app.exec()
