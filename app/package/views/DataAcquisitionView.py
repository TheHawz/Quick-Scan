# This Python file uses the following encoding: utf-8
import numpy as np
import cv2
import os
import queue

from PySide2.QtWidgets import QMainWindow
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import QEvent, Slot

from ..services.CameraThread import CameraThread
from ..services.MicThread import MicThread
from ..models.ActualProjectModel import ActualProjectModel
from ..services import file as fileutils

from ..ui.DataAcquisition_ui import Ui_MainWindow as DataAcquisition_ui


class DataAcquisitionView(QMainWindow, DataAcquisition_ui):

    def __init__(self, model, controller, parent=None):
        super(DataAcquisitionView, self).__init__(parent)
        self._model = model
        self._controller = controller

        self.setupUi(self)
        self.connect_to_controller()
        self.connect_to_model()
        self.set_default_values()
        self.installEventFilter(self)

    # region ------------------------ QMainWindow ------------------------

    def open(self):
        self.show()
        self.create_threads()
        self._controller.start_cam_thread()
        self._controller.start_mic_thread()

    def close(self):
        self.stop_threads()
        self.hide()

    def eventFilter(self, obj, event):
        if obj is self and event.type() == QEvent.Close:
            self.stop_threads()
            event.accept()
            return True
        else:
            return super(DataAcquisitionView, self).eventFilter(obj, event)

    def connect_to_controller(self):
        self.start_stop_button.clicked.connect(
            self._controller.toogle_recording)

    def connect_to_model(self):
        self._model.on_mic_thread_runnnig_changed.connect(
            self.handle_mic_thread_runnnig_changed)
        self._model.on_cam_thread_runnnig_changed.connect(
            self.handle_cam_thread_runnnig_changed)
        self._model.on_mic_recording_changed.connect(
            self.handle_mic_recording_changed)
        self._model.on_cam_recording_changed.connect(
            self.handle_cam_recording_changed)

    def set_default_values(self):
        self.q = queue.Queue()

    # endregion

    # region -------------------------- Threads --------------------------

    def create_threads(self):
        # 1. Start camera Thread
        self._model.camThread = CameraThread(self)
        self._model.camThread.update_frame.connect(self.handle_new_image)
        self._model.camThread.on_stop_recording.connect(self.save_positon_data)

        # 2. Start Mic Thread
        self._model.micThread = MicThread(self)
        self._model.micThread.update_volume.connect(self.handle_new_audio)
        self._model.micThread.on_stop_recording.connect(self.handle_rec_ended)

    def stop_threads(self):
        self._controller.stop_mic_thread()
        self._controller.stop_cam_thread()

    # endregion

    # region ------------------------- Handlers --------------------------

    def handle_rec_ended(self):
        self._controller.navigate('display_results')

    @Slot(bool)
    def handle_mic_thread_runnnig_changed(self, value):
        pass

    @Slot(bool)
    def handle_cam_thread_runnnig_changed(self, value):
        pass

    @Slot(object)
    def save_positon_data(self, value):
        ActualProjectModel.data_x = value["x_data"]
        ActualProjectModel.data_y = value["y_data"]

        # Write data to disk
        path = os.path.join(
            ActualProjectModel.project_location, 'Position Data')
        fileutils.mkdir(path)

        fileutils.save_np_to_txt(value["x_data"], path, file_name="x_data.txt")
        fileutils.save_np_to_txt(value["y_data"], path, file_name="y_data.txt")

    def handle_mic_recording_changed(self, rec):
        if not rec:
            print('View: stopped mic recording')
            self.start_stop_button.setText('START!')
        else:
            print('View: started mic recording')
            self.start_stop_button.setText('STOP!')

    def handle_cam_recording_changed(self, rec):
        if not rec:
            print('View: stopped cam recording')
            self.start_stop_button.setText('START!')
        else:
            print('View: started cam recording')
            self.start_stop_button.setText('STOP!')

    # TODO: move to utils
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_format = QImage(
            rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qt_format)

    @Slot(np.ndarray)
    def handle_new_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.cam_view.setPixmap(qt_img)

    @Slot(int)
    def handle_new_audio(self, value):
        self.q.put(value)

    # endregion
