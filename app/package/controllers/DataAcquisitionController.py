from PySide2.QtCore import QObject, Slot


class DataAcquisitionController(QObject):

    def __init__(self, model, navigator):
        super().__init__()
        self._model = model
        self._navigator = navigator

    @Slot(str)
    def navigate(self, value):
        self._navigator.navigator.emit(value)

    def stop_mic_thread(self):
        self._model.mic_thread_running = False

    def stop_cam_thread(self):
        self._model.cam_thread_running = False

    def start_mic_thread(self):
        self._model.micThread.start()
        self._model.mic_thread_running = True

    def start_cam_thread(self):
        self._model.camThread.start()
        self._model.cam_thread_running = True

    def toogle_recording(self):
        self._model.mic_recording = not self._model.mic_recording
        self._model.cam_recording = not self._model.cam_recording
