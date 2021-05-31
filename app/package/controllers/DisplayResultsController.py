import numpy as np

from PySide2.QtCore import QObject, Slot
from ..services.grid import Grid

from app.package.models.DisplayResultsModel import DisplayResultsModel


def log(msg):
    print(f'[Display Results] {msg}')


class DisplayResultsController(QObject):

    def __init__(self, model: DisplayResultsModel, navigator):
        super().__init__()
        self._model = model
        self._navigator = navigator

    @Slot(str)
    def navigate(self, value):
        self._navigator.navigator.emit(value)

    @Slot(np.ndarray)
    def set_data_x(self, value):
        self._model.data_x = value

    @Slot(np.ndarray)
    def set_data_y(self, value):
        self._model.data_y = value

    def set_data(self, value):
        self._model.data_x = value[0]
        self._model.data_y = value[1]

    @Slot(list)
    def set_freq_range(self, value):
        self._model.freq_range = value

    @Slot()
    def set_grid(self, grid_info):
        self._model.grid = Grid(self._model.frame_size,
                                int(grid_info[0]), int(grid_info[1]),
                                int(grid_info[2]))

    @Slot(int)
    def select_row(self, value):
        self._model.row = value

    @Slot(int)
    def select_col(self, value):
        self._model.col = value
