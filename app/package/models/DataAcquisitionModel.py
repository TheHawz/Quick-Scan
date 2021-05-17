from PySide2.QtCore import QObject, Signal


class DataAcquisitionModel(QObject):

    on_mic_thread_runnnig_changed = Signal(bool)
    on_cam_thread_runnnig_changed = Signal(bool)
    on_mic_recording_changed = Signal(bool)
    on_cam_recording_changed = Signal(bool)

    def __init__(self):
        super().__init__()
        self.clear_state()

    def clear_state(self):
        self._mic_thread_running = False
        self._cam_thread_running = False
        self._mic_recording = False
        self._cam_recording = False

    # region Props & Setters
    @property
    def mic_thread_running(self):
        return self._mic_thread_running

    @mic_thread_running.setter
    def mic_thread_running(self, value):
        self._mic_thread_running = value
        self.on_mic_thread_runnnig_changed.emit(value)

    # --- --- --- --- --- --- --- --- --- ---

    @property
    def cam_thread_running(self):
        return self._cam_thread_running

    @cam_thread_running.setter
    def cam_thread_running(self, value):
        self._cam_thread_running = value
        self.on_cam_thread_runnnig_changed.emit(value)

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

    # endregion
