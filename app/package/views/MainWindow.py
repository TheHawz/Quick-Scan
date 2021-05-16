# This Python file uses the following encoding: utf-8
import os

from PySide2.QtWidgets import QMainWindow

from ..ui.Form_ui import Ui_MainWindow as Form_ui

class MainWindow(QMainWindow, Form_ui):

    def __init__(self, model, controller):
        super(MainWindow, self).__init__()
        self._model = model
        self._main_controller = controller
        
        self.setupUi(self)
        self.connect_elements()

    def open(self):
        self.show()

    def close(self):
        self.hide()

    def connect_elements(self):
        pass
