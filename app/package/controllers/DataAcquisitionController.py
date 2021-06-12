from PySide2.QtCore import QObject, Slot
from app.package.models.DataAcquisitionModel import DataAcquisitionModel


def log(msg: str) -> None:
    print('[DataAcquisition/Controller] ' + msg)


class DataAcquisitionController(QObject):

    def __init__(self, model: DataAcquisitionModel, navigator):
        super().__init__()
        self._model = model
        self._navigator = navigator

    @Slot(str)
    def navigate(self, value):
        self._navigator.navigator.emit(value)

    def start_mic_thread(self):
        self._model.micThread.start()
        self._model.mic_thread_running = True

    def start_cam_thread(self, time_of_rec):
        self._model.camThread.start()
        self._model.camThread.set_min_time(time_of_rec)
        self._model.min_time_of_rec = time_of_rec
        self._model.cam_thread_running = True

    def stop_mic_thread(self):
        if self._model.micWorker:
            self._model.micWorker.stop()
        self._model.mic_thread_running = False

    def stop_cam_thread(self):
        if self._model.camThread:
            self._model.camThread.stop()
        self._model.cam_thread_running = False

    def toogle_recording(self):
        rec = self._model.cam_recording

        if rec:
            self._model.micWorker.stop_rec()
            self._model.camThread.stop_rec()
        else:
            self._model.micWorker.rec()
            self._model.camThread.rec()

        self._model.mic_recording = not rec
        self._model.cam_recording = not rec

    def change_rows(self, value):
        self._model.rows = value
        self._model.camThread.setRows(value)

    def change_cols(self, value):
        self._model.cols = value
        self._model.camThread.setCols(value)

    def change_padding(self, value):
        self._model.padding = value
        self._model.camThread.setPadding(value)

    def take_bg_picture(self):
        img = self._model.camThread.last_frame
        if img is None:
            log('[ERROR] while getting picture...')

        self._model.bg_img = img
