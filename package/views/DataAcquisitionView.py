# This Python file uses the following encoding: utf-8
import os
import cv2

from PySide2.QtCore import QEvent, QFile, QThread, Qt, Signal, Slot
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow


class CameraThreat(QThread):
    update_frame = Signal(QImage)

    def run(self):
        self.running = True
        cap = cv2.VideoCapture(0)
        
        while self.running:
            ret, frame = cap.read()
            if not ret: break
            self.send_frame_to_ui(frame)

    def send_frame_to_ui(self, frame):
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        self.update_frame.emit(p)

        
class DataAcquisitionView(QMainWindow):

    def __init__(self, model, controller):
        super(DataAcquisitionView, self).__init__()
        self._model = model
        self._controller = controller

        self.load_ui()
        self.connect_to_controller()
        self.connect_to_model()
        self.set_default_values()
        
        self.th = CameraThreat(self)
        self.th.update_frame.connect(self.setImage)
        self.window.installEventFilter(self)
        
    def open(self):
        self.window.show()
        self.th.start()

    def close(self):
        self.window.hide()
        
    def stop_threat(self):
        self.th.running = False

    def eventFilter(self, obj, event):
        if obj is self.window and event.type() == QEvent.Close:
            self.stop_threat()
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

    @Slot(QImage)
    def setImage(self, value):
        self.window.cam_view.setPixmap(QPixmap.fromImage(value))
