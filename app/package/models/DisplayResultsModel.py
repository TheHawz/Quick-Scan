import numpy as np

from PySide2.QtCore import QObject, Signal


class DisplayResultsModel(QObject):

    # Signals: to announce changes to the View
    data_x_changed = Signal(np.ndarray)
    data_y_changed = Signal(np.ndarray)
    audio_data_changed = Signal(list)
    audio_fs_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.clear_state()

    def clear_state(self):
        self._data_x = np.array([])
        self._data_y = np.array([])

    # region Props & Setters
    @property
    def data_x(self):
        return self._data_x

    @data_x.setter
    def data_x(self, value):
        self._data_x = value
        self.data_x_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def data_y(self):
        return self._data_y

    @data_y.setter
    def data_y(self, value):
        self._data_y = value
        self.data_y_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def freq_range(self):
        return self._freq_range

    @freq_range.setter
    def freq_range(self, value):
        self._freq_range = value
        self.freq_range.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def audio_data(self):
        return self._audio_data

    @audio_data.setter
    def audio_data(self, value):
        self._audio_data = value
        self.audio_data_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def audio_fs(self):
        return self._audio_fs

    @audio_fs.setter
    def audio_fs(self, value):
        self._audio_fs = int(value)
        self.audio_fs_changed.emit(int(value))

    # endregion
