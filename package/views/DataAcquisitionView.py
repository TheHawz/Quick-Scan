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

from PySide2.QtCore import QEvent, QFile, QThread, Qt, Signal, Slot
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow, QWidget

from ..models.ActualProjectModel import ActualProjectModel

# from ..services import colorSegmentation as cs  # Credits to Lara!
from ..services.grid import Grid
from ..services import imbasic as imb
from ..services import colorSegmentation as cs
from ..services.path import interpolate_nan
from ..services.mask import get_mask, get_circles

assert numpy  # avoid "imported but unused" message (W0611)
q = queue.Queue()

# TODO: move to own file
# GRID DEFINITION
NUMBER_OF_ROWS = 8
NUMBER_OF_COLS = 8
PADDING = 100


class CameraThread(QThread):
    update_frame = Signal(np.ndarray)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x_data = []
        self.y_data = []

    def run(self):
        """Callback function executed whenever someone starts the QThreat (thread.start())
        """
        self._running = True
        self._rec = False

        cap = cv2.VideoCapture(ActualProjectModel.video_device)

        self.frame_size = np.array([int(cap.get(3)), int(cap.get(4))])
        self._grid = Grid(self.frame_size, NUMBER_OF_ROWS,
                          NUMBER_OF_COLS, padding=20)

        while self._running:
            ret, frame = cap.read()

            if not ret:
                break

            if not self._rec:
                self._grid.config(NUMBER_OF_ROWS, NUMBER_OF_COLS, padding=20)

            processed_frame = self.process_frame(frame)
            self.update_frame.emit(processed_frame)

        print('Stopping Camera Thread!')
        cap.release()

    def process_circles(self, frame, circles):
        """Appends data to the arrays and draws circles in the frame

        Args:
            frame ([type]): [description]
            circles ([type]): [description]
        """
        if circles is None:
            if len(self.x_data) != 0:
                self.x_data.append(np.nan)
                self.y_data.append(np.nan)
        else:
            circles = np.round(circles[0, :]).astype("int")

            for (x, y, r) in circles:
                self.x_data.append(x)
                self.y_data.append(y)
                frame = cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                frame = cv2.rectangle(
                    frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                break

    def process_frame(self, frame):
        """Process each frame

        Args:
            frame ([type]): [description]

        Returns:
            [type]: [description]
        """

        # mask = get_mask(frame)
        # circles = get_circles(mask)
        # draw_grid(frame, NUMBER_OF_ROWS, NUMBER_OF_COLS, PADDING)
        self._grid.draw_grid(frame)
        # self.process_circles(frame, circles)

        return frame

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._running = False
        self.wait()


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata.copy())


class MicThread(QThread):
    update_volume = Signal(int)

    def __init__(self, rate=4000, chunksize=1024, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rate = rate
        self.chunksize = chunksize
        self.device = ""
        self.stream = sd.InputStream(
            device=(1, 3), channels=2,
            samplerate=44100, callback=callback)

    def run(self):
        self._running = True

        try:
            with self.stream:
                pass
        except KeyboardInterrupt:
            print("[MICTHREAD] KeyboardInterrupt")
            self.stop()
        except Exception as e:
            print("[MICTHREAD] Exception: ", e)
            self.stop()

        print("[MICTHREAD] Finished!")

    def stop(self):
        self._running = False
        self.wait()


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

        return super(DataAcquisitionView, self).eventFilter(obj, event)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join('designer', "data_acquisition.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()

    def connect_to_controller(self):
        pass

    def connect_to_model(self):
        pass

    def set_default_values(self):
        pass

    def start_threads(self):
        self.cameraThread = CameraThread(self)
        self.cameraThread.update_frame.connect(self.set_image)
        self.micThread = MicThread(self)
        self.micThread.update_volume.connect(self.set_volume)
        self.window.installEventFilter(self)

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
        if value:
            print(value)
