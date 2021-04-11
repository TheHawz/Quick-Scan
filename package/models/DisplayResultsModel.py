import numpy as np

from PySide2.QtCore import QObject, Signal


class DisplayResultsModel(QObject):

    # Signals: to announce changes to the View
    data_x_changed = Signal()
    data_y_changed = Signal()

    def __init__(self):
        super().__init__()
        self.clear_state()

    def clear_state(self):
        self._data_x = np.array([])
        self._data_y = np.array([])

    # Props & Setters
    @property
    def data_x(self):
        return self._data_x

    @data_x.setter
    def data_x(self, value):
        self._data_x = value
        self.data_x_changed.emit()

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def data_y(self):
        return self._data_y

    @data_y.setter
    def data_y(self, value):
        self._data_y = value
        self.data_y_changed.emit()
