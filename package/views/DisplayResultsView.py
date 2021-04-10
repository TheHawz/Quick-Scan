# This Python file uses the following encoding: utf-8
import os

from PySide2.QtWidgets import QMainWindow, QFileDialog
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader

from ..models.ActualProjectModel import ActualProjectModel


class DisplayResultsView(QMainWindow):
    def __init__(self, model, controller):
        super(DisplayResultsView, self).__init__()
        self._model = model
        self._controller = controller

        self.load_ui()
        self.connect_to_controller()
        self.connect_to_model()
        self.set_default_values()

    def open(self):
        self.window.show()
        self.onOpen()

    def close(self):
        self.window.hide()

    # region HELPER FUNCTIONS AND CALLBACKS

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join('designer', "display_results.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()

    def connect_to_controller(self):
        pass

    def connect_to_model(self):
        pass

    def set_default_values(self):
        pass

    def onOpen(self):
        self._controller.setData(ActualProjectModel.data_x,
                                 ActualProjectModel.data_y)
        pass

    # endregion
