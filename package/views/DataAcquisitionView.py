# This Python file uses the following encoding: utf-8
import tempfile
import numpy  # Make sure NumPy is loaded before it is used in the callback
# import soundfile as sf
import sounddevice as sd
import sys
import queue
import os
import cv2
import numpy as np
import time

from PySide2.QtCore import QEvent, QFile, QThread, Qt, Signal, Slot
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow, QWidget

from ..models.ActualProjectModel import ActualProjectModel

# from ..services import colorSegmentation as cs  # Credits to Lara!
from ..services.CameraThread import CameraThread
from ..services.grid import Grid
from ..services import imbasic as imb
from ..services import colorSegmentation as cs
from ..services.path import interpolate_nan
from ..services.mask import get_mask, get_circles

# assert numpy  # avoid "imported but unused" message (W0611)


class MicThread(QThread):
    update_volume = Signal(object)

    def __init__(self, rate=44100, chunksize=1024, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rate = rate
        self.chunksize = chunksize
        self.device = ""
        self.q = queue.Queue()

        self.stream = sd.InputStream(
            device=(1, 3), channels=2, samplerate=44100, callback=self.callback, blocksize=1024)

    def run(self):
        self._running = True

        try:
            print("[MICTHREAD] Trying...")
            with self.stream:
                if not self._running:
                    raise KeyboardInterrupt()

        except KeyboardInterrupt:
            print("[MICTHREAD] KeyboardInterrupt")
            # self.stop()
        except Exception as e:
            print("[MICTHREAD] Exception: ", e)
            # self.stop()

        print("[MICTHREAD] Finished!")

    def stop(self):
        print("Stopping audio stream")
        self.stream.stop()
        self._running = False
        self.wait()
        # return KeyboardInterrupt()

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        # print('.')
        self.q.put(indata.copy())
        self.update_volume.emit(indata.copy())


class DataAcquisitionView(QMainWindow):

    def __init__(self, model, controller, parent=None):
        super(DataAcquisitionView, self).__init__(parent)
        self._model = model
        self._controller = controller

        self.load_ui()
        self.connect_to_controller()
        self.connect_to_model()
        self.set_default_values()
        self.start_threads()
        self.installEventFilter(self)

    def open(self):
        self.window.show()
        self.start_thread()

    def close(self):
        self.stop_thread()
        self.window.hide()

    def start_thread(self):
        self.cameraThread.start()
        self.micThread.start()

    def stop_thread(self):
        self.cameraThread.stop()
        self.micThread.stop()

    def eventFilter(self, obj, event):
        if obj is self.window and event.type() == QEvent.Close:
            self.stop_thread()
            event.accept()
            return True
        else:
            return super(DataAcquisitionView, self).eventFilter(obj, event)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join('designer', "data_acquisition.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()

    def connect_to_controller(self):
        self.window.start_stop_button.clicked.connect(self.start_stop)

    def connect_to_model(self):
        pass

    def set_default_values(self):
        pass

    def start_threads(self):
        # 1. Start camera Thread
        self.cameraThread = CameraThread(self)
        self.cameraThread.update_frame.connect(self.set_image)
        self.cameraThread.on_stop_recording.connect(
            self.stop_recording_handler)

        # 2. Start Mic Thread
        self.micThread = MicThread(self)
        self.micThread.update_volume.connect(self.set_volume)
        self.window.installEventFilter(self)

    @Slot(object)
    def stop_recording_handler(self, value):
        self.stop_thread()  # change
        ActualProjectModel.data_x = value["x_data"]
        ActualProjectModel.data_y = value["y_data"]
        self._controller.navigate('display_results')

    @Slot(np.ndarray)
    def set_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.window.cam_view.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_format = QImage(
            rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # p = qt_format.scaled(
        #     self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(qt_format)

    @Slot(int)
    def set_volume(self, value):
        pass
        # print(len(value))

    def start_stop(self):
        self.cameraThread.toogleRec()
