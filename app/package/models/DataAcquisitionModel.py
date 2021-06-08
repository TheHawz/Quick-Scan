import numpy as np

from PySide2.QtCore import QObject, QThread, Signal

from app.package.services.MicWorker import MicWorker
from app.package.services.CameraThread import CameraThread


class DataAcquisitionModel(QObject):

    on_mic_thread_running_changed = Signal(bool)
    on_cam_thread_running_changed = Signal(bool)
    on_mic_recording_changed = Signal(bool)
    on_cam_recording_changed = Signal(bool)
    on_min_time_of_rec_changed = Signal(float)
    on_rows_changed = Signal(int)
    on_cols_changed = Signal(int)
    on_padding_changed = Signal(int)
    on_bg_img_changed = Signal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.clear_state()

    def clear_state(self):
        self._mic_thread_running = False
        self._cam_thread_running = False
        self._mic_recording = False
        self._cam_recording = False
        self.micWorker: MicWorker = None
        self.micThread: QThread = None
        self.camThread: CameraThread = None
        self._bg_img: np.ndarray = None

    def get_grid_as_list(self):
        return [self.rows, self.cols, self.padding]

    # region Props & Setters

    @property
    def mic_thread_running(self):
        return self._mic_thread_running

    @mic_thread_running.setter
    def mic_thread_running(self, value):
        self._mic_thread_running = value
        self.on_mic_thread_running_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def cam_thread_running(self):
        return self._cam_thread_running

    @cam_thread_running.setter
    def cam_thread_running(self, value):
        self._cam_thread_running = value
        self.on_cam_thread_running_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def mic_recording(self):
        return self._mic_recording

    @mic_recording.setter
    def mic_recording(self, value):
        self._mic_recording = value
        self.on_mic_recording_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def cam_recording(self):
        return self._cam_recording

    @cam_recording.setter
    def cam_recording(self, value):
        self._cam_recording = value
        self.on_cam_recording_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def min_time_of_rec(self):
        return self._min_time_of_rec

    @min_time_of_rec.setter
    def min_time_of_rec(self, value):
        self._min_time_of_rec = value
        self.on_min_time_of_rec_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value
        self.on_rows_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def cols(self):
        return self._cols

    @cols.setter
    def cols(self, value):
        self._cols = value
        self.on_cols_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, value):
        self._padding = value
        self.on_padding_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def bg_img(self):
        return self._bg_img

    @bg_img.setter
    def bg_img(self, value):
        self._bg_img = value
        self.on_bg_img_changed.emit(value)

    # endregion
