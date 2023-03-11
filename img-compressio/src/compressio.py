import os
from multiprocessing.pool import ThreadPool
from PIL import Image
from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QThread
from compressio_gui import Ui_Form


class Worker(QThread):
    '''
    This class is responsible for batch image processing itself.
    '''
    finished = pyqtSignal()
    success = pyqtSignal(int)
    empty_entries_error = pyqtSignal()
    incorrect_path_error = pyqtSignal()
    progress = pyqtSignal()

    def run(self):

        # 'return' keyword in the except body stops the function
        try:
            win.get_sources()
        except ValueError:
            self.empty_entries_error.emit()
            return
        except FileNotFoundError:
            self.incorrect_path_error.emit()
            return

        win.quality = win.ui.qualitySpinbox.value()

        # Saves image in a format, chosen in a spinbox, if the value in the spinbox != "Original"
        # if it is, format remains the same
        self.img_format = win.ui.formatBox.currentText().lower(
        ) if win.ui.formatBox.currentText() != "Original" else None

        extensions = (".png", ".jpg", ".jpeg", ".bmp", ".jfif")
        files = [file for file in os.scandir(
            win.source_dir) if file.endswith(extensions)]

        win.ui.progressBar.setMaximum(len(files))

        p = ThreadPool()
        pool_map = p.map(self.process_file, files)

        p.close()
        p.join()

        self.success.emit(len(pool_map))
        self.finished.emit()

    def process_file(self, file):
        fname, fext = os.path.splitext(file)

        fext = f'.{self.img_format}' if self.img_format is not None else fext

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
        self.setWindowIcon(QIcon("icon.ico"))

        # These attributes are made to avoid passing directories from method to method
        self.source_dir = None
        self.dest_dir = None
        self.quality = 75

        self.ui.sourceBtn.clicked.connect(self.open_source_directory)
        self.ui.destinationBtn.clicked.connect(self.open_dest_directory)

        self.ui.proceedAllBtn.clicked.connect(self.proceed_all)

        self.worker = Worker()

    def show_done_message(self, counter):
        qtw.QMessageBox.information(
            self, "Success", f"Done! Successfully edited images: {counter}")

    def show_empty_fields_error(self):
        qtw.QMessageBox.warning(self, "Fail", "Fields cannot be empty!")

    def show_incorrect_path_error(self):
        qtw.QMessageBox.warning(
            self, "Fail", f"One or both paths are incorrect! \nSource: {self.source_dir} \nDestination: self.dest_dir")

    def open_source_directory(self):
        if directory := qtw.QFileDialog.getExistingDirectory(
            self, "Choose Directory", "", qtw.QFileDialog.DontUseNativeDialog
        ):
            self.ui.sourceEntry.setText(directory)

    def open_dest_directory(self):
        if directory := qtw.QFileDialog.getExistingDirectory(
            self, "Choose Directory", "", qtw.QFileDialog.DontUseNativeDialog
        ):
            self.ui.destinationEntry.setText(directory)

    # Overwrites empty sourceDir and destDir attributes with directories from the input fields
    # If any of the fields is empty - raise an exception that will be caught
    def get_sources(self):

        # 'r' in front of string means raw string. It will ignore escape sequences
        self.source_dir = f"{self.ui.sourceEntry.text()}/"

        # If overwriting checkbox is ticked, dest_dir is same as source_dir
        if self.ui.overwriteCheck.isChecked():
            self.dest_dir = self.source_dir
        else:
            self.dest_dir = f"{self.ui.destinationEntry.text()}/"

        if self.source_dir == '/' or self.dest_dir == '/':
            raise ValueError()

        if os.path.isdir(self.source_dir) is not True or os.path.isdir(self.dest_dir) is not True:
            raise FileNotFoundError()

    def proceed_all(self):
        '''
        Creates separate thread and instantiating Worker class in it.
        Messaboxes, progressbar and counter are updating via Qt signals.
        '''

        self.worker.finished.connect(self.nullify_progress)

        self.worker.success.connect(self.show_done_message)
        self.worker.empty_entries_error.connect(self.show_empty_fields_error)
        self.worker.incorrect_path_error.connect(
            self.show_incorrect_path_error)
        self.worker.progress.connect(self.record_progress)

        self.worker.start()

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
