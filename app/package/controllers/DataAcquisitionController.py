from PySide2.QtCore import QObject, Slot


class DataAcquisitionController(QObject):

    def __init__(self, model, navigator):
        super().__init__()
        self._model = model
        self._navigator = navigator

    @Slot(str)
    def navigate(self, value):
        self._navigator.navigator.emit(value)

    def start_mic_thread(self):
        self._model.micThread.start()
        self._model.mic_thread_running = True

    def start_cam_thread(self):
        self._model.camThread.start()
        self._model.cam_thread_running = True

    def stop_mic_thread(self):
        if self._model.micThread:
            self._model.micThread.stop()
        self._model.mic_thread_running = False

    def stop_cam_thread(self):
        if self._model.camThread:
            self._model.camThread.stop()
        self._model.cam_thread_running = False

    def toogle_recording(self):
        rec = self._model.cam_recording

        if rec:
            self._model.micThread.stop_rec()
            self._model.camThread.stop_rec()
        else:
            # self.start_mic_thread()
            self._model.micThread.rec()
            self._model.camThread.rec()

        self._model.mic_recording = not rec
        self._model.cam_recording = not rec
