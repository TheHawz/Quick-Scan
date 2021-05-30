# This Python file uses the following encoding: utf-8
import os

from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import Slot

from ..controllers.Calibrate_controller import CalibrateController
from ..models.Calibrate_model import CalibrateModel
from ..ui.Calibrate_ui import Ui_MainWindow as Calibrate_ui


class CalibrateView(QMainWindow, Calibrate_ui):

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
        pass

    def connect_to_model(self):
        pass

    def set_default_values(self):
        pass

    # region SLOTS

    # endregion
