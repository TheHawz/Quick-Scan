# This Python file uses the following encoding: utf-8
import os

from PySide2.QtWidgets import  QMainWindow, QFileDialog
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader


class NewProjectView(QMainWindow):

    def __init__(self, model, controller):
        super(NewProjectView, self).__init__()
        self._model = model
        self._controller = controller

        self.load_ui()
        self.connect_to_controller()
        self.connect_to_model()

        # Set Default Values
        self._controller.change_project_location(os.path.expanduser("~"))
        self._controller.change_project_name('New Project')

    def open(self):
        self.window.show()

    def close(self):
        self.window.hide()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join('designer', "new_project.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()

    def connect_to_controller(self):
        self.window.but_create.clicked.connect(lambda: self._controller.navigate('new_project'))
        self.window.line_project_name.textChanged.connect(self._controller.change_project_name)
        self.window.line_project_location.textChanged.connect(self._controller.change_project_location)
        self.window.open_location.clicked.connect(self.open_location_dialog)

    def connect_to_model(self):
        self._model.project_name_changed.connect(self.on_project_name_changed)
        self._model.project_location_changed.connect(self.on_project_location_changed)

    def open_location_dialog(self):
        _dir = str(QFileDialog.getExistingDirectory(self, "Choose a location.", str(self._model.project_location)))
        self._controller.change_project_location(_dir)

    @Slot(str)
    def on_project_name_changed(self, value):
        self.window.line_project_name.setText(value)

    @Slot(str)
    def on_project_location_changed(self, value):
        self.window.line_project_location.setText(value)
