# This Python file uses the following encoding: utf-8
import os

from PySide2.QtWidgets import  QMainWindow
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class DataAcquisitionView(QMainWindow):

    def __init__(self, model, controller):
        super(DataAcquisitionView, self).__init__()
        self._model = model
        self._controller = controller

        self.load_ui()
        self.connect_to_controller()
        self.connect_to_model()
        self.set_default_values()

    def open(self):
        self.window.show()

    def close(self):
        self.window.hide()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join('designer', "data_acquisition.ui")
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
