# This Python file uses the following encoding: utf-8
import os
import numpy as np
import sounddevice as sd

from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import QObject, Signal, QThread, Slot

from ..controllers.Calibrate_controller import CalibrateController
from ..models.Calibrate_model import CalibrateModel
from ..ui.Calibrate_ui import Ui_MainWindow as Calibrate_ui
from ..services.dsp import _getTime


class CalibrationWorker(QObject):
    finished = Signal()
    update_status = Signal(str)

    @staticmethod
    def log(msg: str) -> None:
        print(f'[CalibrationWorker] {msg}')

    def process(self, targetSpl, range=[50, 20000]):
        self.log('Processing')
        self.log(targetSpl)

        # t = _getTime(B=range[1]-range[0], e=0.1)
        t = 5
        fs = 44100
        self.log(f'Time rec: {t}')

        x = sd.rec(int(t * fs), channels=1)
        sd.wait()

        spl = 20 * np.log10(np.std(x) / 2e-5)
        self.log(f'Got: {spl}')

        self.log(f'Expected: {targetSpl}')

        self.finished.emit()


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
        pass

    def connect_to_model(self):
        pass

    def set_default_values(self):
        pass

    # region SLOTS

    @Slot()
    def start_calibration(self):
        try:
            spl = int(self.spl_value.text())
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
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        self.thread = thread
        self.thread.start()

    @Slot(str)
    def handle_update_status(self, value):
        print(value)

    # endregion
