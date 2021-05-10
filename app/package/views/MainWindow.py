# This Python file uses the following encoding: utf-8
import os

from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class MainWindow(QMainWindow):

    def __init__(self, model, controller):
        super(MainWindow, self).__init__()
        self._model = model
        self._main_controller = controller
        self.load_ui()
        self.connect_elements()

    def open(self):
        self.window.show()

    def close(self):
        self.window.hide()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join('resources', 'ui', "Form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, self)
        ui_file.close()

    def connect_elements(self):
        pass
        # self.window.nav_but_1.clicked.connect(lambda: self._main_controller.navigate('new_project'))
