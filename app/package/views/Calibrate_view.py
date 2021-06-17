# This Python file uses the following encoding: utf-8
from app.package.models.ActualProjectModel import ActualProjectModel
import os
import numpy as np
import sounddevice as sd

from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import QObject, Signal, QThread, Slot

from ..controllers.Calibrate_controller import CalibrateController
from ..models.Calibrate_model import CalibrateModel
from ..ui.Calibrate_ui import Ui_MainWindow as Calibrate_ui
from ..services.file import save_np_to_txt


def get_documents_dir():
    import platform
    if platform.system() == 'Windows':
        import ctypes.wintypes
        CSIDL_PERSONAL = 5       # My Documents
        SHGFP_TYPE_CURRENT = 0   # Get current, not default value

        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(
            None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

        return buf.value


class CalibrationWorker(QObject):
    finished = Signal()
    update_status = Signal(str)

    @staticmethod
    def log(msg: str) -> None:
        print(f'[CalibrationWorker] {msg}')

    def process(self, targetSpl):
        self.log('Processing')
        self.log(targetSpl)

        t = 5
        sd.default.samplerate = fs = 44100
        self.log(f'Time rec: {t}')

        # x = sd.rec(int(t * fs), channels=2)

        x = sd.rec(frames=int(t*fs), channels=1)
        sd.wait()
        x = np.sum(x, 1)  # change

        # print(np.max(x))
        # rms = np.sqrt(np.mean(np.square(x)))
        spl = 20*np.log10(np.std(x)/2e-5)

        self.save_calibration_file(spl, targetSpl)
        self.finished.emit()

    def save_calibration_file(self, actual_spl, expected_spl):
        self.log(f'Got: {actual_spl} dB')
        self.log(f'Expected: {expected_spl} dB')

        ActualProjectModel.calibration = {
            'actual': actual_spl, 'expected': expected_spl
        }

        path = os.path.join(get_documents_dir(), 'Scan&Paint Clone')
        file_name = 'calibration.dat'
        save_np_to_txt(np.array([expected_spl, actual_spl]), path, file_name)


class CalibrateView(QMainWindow, Calibrate_ui):

    @staticmethod
    def log(msg):
        print(f'[Calibrate/View] {msg}')

    def __init__(self, model: CalibrateModel, controller: CalibrateController):
        super(CalibrateView, self).__init__()
        self._model = model
        self._controller = controller

        self.setupUi(self)
        self.connect_to_controller()
        self.connect_to_model()
        self.set_default_values()

    def open(self):
        self.show()

    def close(self):
        self.hide()

    def connect_to_controller(self):
        self.calibrate_button.clicked.connect(self.start_calibration)
        self.go_back_button.clicked.connect(self._controller.go_back)
        pass

    def connect_to_model(self):
        pass

    def set_default_values(self):
        title = "Quick Scan: Calibrate"
        self.setWindowTitle(title)

    # region SLOTS

    @Slot()
    def start_calibration(self):
        try:
            spl = float(self.spl_value.text())
        except Exception:
            self.log(f'Could not convert {self.spl_value.text()} to int')

        # Create worker and thread
        worker = CalibrationWorker()
        thread = QThread()
        worker.moveToThread(thread)

        # Conect the 'started' signal of the Thread
        # to the corresponding function in the worker
        thread.started.connect(lambda: worker.process(spl))
        worker.update_status.connect(self.handle_update_status)

        # Connect the finished signal of thread & worker
        # with the corresponding stuff
        worker.finished.connect(thread.quit)
        worker.finished.connect(self.go_back)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        self.thread = thread
        self.thread.start()

    @Slot(str)
    def handle_update_status(self, value):
        print(value)

    @Slot()
    def go_back(self):
        self._controller._navigator.navigate('new_project')

    # endregion
