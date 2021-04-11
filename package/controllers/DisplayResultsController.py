import numpy as np

from PySide2.QtCore import QObject, Slot


class DisplayResultsController(QObject):

    def __init__(self, model, navigator):
        super().__init__()
        self._model = model
        self._navigator = navigator

    @Slot(str)
    def navigate(self, value):
        self._navigator.navigator.emit(value)

    @Slot(np.array)
    def set_data_x(self, value):
        self._model.data_x = value

    @Slot(np.array)
    def set_data_y(self, value):
        self._model.data_y = value
