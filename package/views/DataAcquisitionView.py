# This Python file uses the following encoding: utf-8
import os
import cv2
import numpy as np

from PySide2.QtCore import QEvent, QFile, QThread, Qt, Signal, Slot
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow, QWidget

from ..models.ActualProjectModel import ActualProjectModel

from ..services import colorSegmentation as cs  # Credits to Lara!
from ..services.grid import Grid, draw_grid
from ..services import imbasic as imb
from ..services import colorSegmentation as cs
from ..services.path import interpolate_nan
from ..services.mask import improve_mask

# TODO: move to own file
TRACKING_COLOR = (220, 198, 43)  # BGR
BOTTOM_HSV_THRES = (80, 110, 10)
TOP_HSV_THRES = (130, 255, 255)

# TODO: move to own file
# GRID DEFINITION
NUMBER_OF_ROWS = 8
NUMBER_OF_COLS = 8
PADDING = 100


class CameraThread(QThread):
    update_frame = Signal(QImage)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x_data = []
        self.y_data = []

    def run(self):
        self.running = True
        cap = cv2.VideoCapture(ActualProjectModel.video_device)
        
        while self.running:
            ret, frame = cap.read()
            if not ret: break
            self.send_frame_to_ui(self.process_frame(frame))
        print('Closing!')

    def process_frame(self, frame):
        mask = cs.getColorMask(frame, BOTTOM_HSV_THRES, TOP_HSV_THRES)
        mask = improve_mask(mask, cv2.MORPH_ELLIPSE, (7, 7))

        circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, dp=3, minDist=150)
        
        frame = draw_grid(frame, NUMBER_OF_ROWS, NUMBER_OF_COLS, PADDING)
        
        if circles is None:
            if len(self.x_data) != 0:
                self.x_data.append(np.nan)
                self.y_data.append(np.nan)
        else:
            circles = np.round(circles[0, :]).astype("int")
            
            for (x, y, r) in circles:
                frame = cv2.circle(frame, (x, y), r, (0, 255, 0), 4)                
                self.x_data.append(x)
                self.y_data.append(y)
                frame = cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                break
        
        return frame

    def send_frame_to_ui(self, frame):
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        self.update_frame.emit(p)

        
class MicThread(QThread):
    update_volume = Signal(int)

    def run(self):
        print('Audio Driver: ', ActualProjectModel.audio_driver)
        print('Audio Device: ', ActualProjectModel.audio_device)

        
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
        self.cameraThread.running = False

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
        
    @Slot(QImage)
    def set_image(self, value):
        if value:
            self.window.cam_view.setPixmap(QPixmap.fromImage(value))

    @Slot(int)
    def set_volume(self, value):
        if value:
            print(value)
