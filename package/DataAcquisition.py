# This Python file uses the following encoding: utf-8
import os

from PySide2.QtWidgets import  QWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class DataAcquisition(QWidget):

    def __init__(self, model, controller):
        super(DataAcquisition, self).__init__()
        self._model = model
        self._main_controller = controller
        self.load_ui()
        self.connect_elements()

    def open(self):
        self.show()

    def close(self):
        self.hide()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join('designer', "recording_screen.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, self)
        ui_file.close()

    def connect_elements(self):
        self.window.pushButton.clicked.connect(lambda: self._main_controller.navigate('main_view'))


