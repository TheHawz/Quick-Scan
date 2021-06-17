import numpy as np

from PySide2.QtCore import QObject, Signal
# from ..services.DspThread import DspThread
from ..services.grid import Grid


class DisplayResultsModel(QObject):

    # Signals: to announce changes to the View
    on_data_x_changed = Signal(np.ndarray)
    on_data_y_changed = Signal(np.ndarray)
    on_audio_data_changed = Signal(list)
    on_audio_fs_changed = Signal(int)
    on_freq_range_changed = Signal(list)
    on_grid_changed = Signal(object)
    on_thread_status_update = Signal(int)
    on_image_changed = Signal(object)
    on_row_changed = Signal(int)
    on_col_changed = Signal(int)
    on_freq_changed = Signal(object)
    on_full_band_spec_changed = Signal(object)
    on_spectrum_changed = Signal(object)

    def __init__(self):
        super().__init__()
        self.clear_state()

    def clear_state(self):
        self._data_x = np.array([])
        self._data_y = np.array([])
        self._grid: Grid = None
        self._audio_data = []
        self._audio_fs = -1
        self._fps = -1
        self._image = np.array([])
        self.dsp_thread = None
        self._spectrum = []
        self._freq = []
        self._row = -1
        self._col = -1
        self._full_band_spec = []
        self.min_db = 40
        self.max_db = 90

    # region Props & Setters

    @property
    def data_x(self):
        return self._data_x

    @data_x.setter
    def data_x(self, value):
        self._data_x = value
        self.on_data_x_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def data_y(self):
        return self._data_y

    @data_y.setter
    def data_y(self, value):
        self._data_y = value
        self.on_data_y_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def freq_range(self):
        return self._freq_range

    @freq_range.setter
    def freq_range(self, value):
        self._freq_range = value
        self.on_freq_range_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def audio_data(self):
        return self._audio_data

    @audio_data.setter
    def audio_data(self, value):
        self._audio_data = value
        self.on_audio_data_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def audio_fs(self):
        return self._audio_fs

    @audio_fs.setter
    def audio_fs(self, value):
        self._audio_fs = int(value)
        self.on_audio_fs_changed.emit(int(value))

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, value: Grid):
        self._grid = value
        self.on_grid_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, value):
        self._fps = value

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
        self.on_image_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        self._row = value
        self.on_row_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, value):
        self._col = value
        self.on_col_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, value):
        self._freq = value
        self.on_freq_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def spectrum(self):
        return self._spectrum

    @spectrum.setter
    def spectrum(self, value):
        self._spectrum = value
        self.check_max_min()
        self.on_spectrum_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def full_band_spec(self):
        return self._full_band_spec

    @full_band_spec.setter
    def full_band_spec(self, value):
        self._full_band_spec = value
        self.check_max_min()
        self.on_full_band_spec_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    def check_max_min(self):

        if len(self._full_band_spec) > 0:
            self.min_db = np.min([self.min_db,
                                 np.array(self._full_band_spec).min()])
            self.max_db = np.max([self.max_db,
                                 np.array(self._full_band_spec).max()])

        if len(self._spectrum) > 0:
            self.min_db = np.min([self.min_db,
                                 np.array(self._spectrum).min()])
            self.max_db = np.max([self.max_db,
                                 np.array(self._spectrum).max()])

        self.min_db = int(np.floor(self.min_db))
        self.max_db = int(np.ceil(self.max_db))

    # endregion
