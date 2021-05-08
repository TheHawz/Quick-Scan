# This Python file uses the following encoding: utf-8
import numpy as np
import cv2
import os
import queue

from PySide2.QtWidgets import QMainWindow
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import QEvent, QFile, QThread,  Signal, Slot

from ..services.CameraThread import CameraThread
from ..services.MicThread import MicThread
from ..models.ActualProjectModel import ActualProjectModel

# TODO: add regions


class DataAcquisitionView(QMainWindow):

    def __init__(self, model, controller, parent=None):
        super(DataAcquisitionView, self).__init__(parent)
        self._model = model
        self._controller = controller

        self.load_ui()
        self.connect_to_controller()
        self.connect_to_model()
        self.set_default_values()
        self.installEventFilter(self)

    # region ------------------------ QMainWindow ------------------------

    def open(self):
        self.window.show()
        self.create_threads()
        self.start_thread()

    def close(self):
        self.stop_thread()
        self.window.hide()

    def eventFilter(self, obj, event):
        if obj is self.window and event.type() == QEvent.Close:
            self.stop_thread()
            event.accept()
            return True
        else:
            return super(DataAcquisitionView, self).eventFilter(obj, event)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join('resources', 'ui', "data_acquisition.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()

    def connect_to_controller(self):
        self.window.start_stop_button.clicked.connect(self.start_stop)

    def connect_to_model(self):
        pass

    def set_default_values(self):
        self.q = queue.Queue()

    # endregion

    # region -------------------------- Threads --------------------------

    def create_threads(self):
        # 1. Start camera Thread
        self.cameraThread = CameraThread(self)
        self.cameraThread.update_frame.connect(self.set_image)
        self.cameraThread.on_stop_recording.connect(
            self.stop_recording_handler)

        # 2. Start Mic Thread
        self.micThread = MicThread(self)
        self.micThread.update_volume.connect(self.set_volume)
        self.window.installEventFilter(self)

    def start_thread(self):
        self.cameraThread.start()
        # self.micThread.start()

    def stop_thread(self):
        if hasattr(self, 'cameraThread'):
            self.cameraThread.stop()
        if hasattr(self, 'micThread'):
            self.micThread.stop()

    # endregion

    # region ------------------------- Handlers --------------------------

    @Slot(object)
    def stop_recording_handler(self, value):
        self.stop_thread()  # change
        ActualProjectModel.data_x = value["x_data"]
        ActualProjectModel.data_y = value["y_data"]

        # Write data to disk!
        self.save_np_to_txt(value["x_data"], file_name="x_data.txt")
        self.save_np_to_txt(value["y_data"], file_name="y_data.txt")
        self._controller.navigate('display_results')

    # TODO: move to own file
    @staticmethod
    def save_np_to_txt(data, file_name="data.txt", path=os.path.join("data"), add_date_prefix=True):
        if add_date_prefix:
            from datetime import datetime

            now = datetime.now()
            date = now.strftime("[%Y-%m-%d_%H%M%S] ")
            file_name = date + file_name

        file_path = os.path.join(path, file_name)
        np.savetxt(file_path, data)

    def start_stop(self):
        self.cameraThread.toogleRec()
        self.micThread.toogleRec()
        self.micThread.start()

    # TODO: move to utils
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_format = QImage(
            rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # p = qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(qt_format)

    @Slot(np.ndarray)
    def set_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.window.cam_view.setPixmap(qt_img)

    @Slot(int)
    def set_volume(self, value):
        self.q.put(value)

    # endregion
