from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import QFileDialog


class NewProjectController(QObject):

    navigator = Signal(str)

    def __init__(self, model):
        super().__init__()
        self._model = model

    @Slot(str)
    def navigate(self, value):
        self.navigator.emit(value)

    @Slot(str)
    def change_project_name(self, value):
        self._model.project_name = value

    @Slot(str)
    def change_project_location(self, value):
        self._model.project_location = value
