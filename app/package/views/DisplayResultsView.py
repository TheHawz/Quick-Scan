# This Python file uses the following encoding: utf-8
import numpy as np
import cv2

from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import Slot
from PySide2.QtGui import QImage, QPixmap

from ..models.ActualProjectModel import ActualProjectModel
from ..ui.DisplayResults_ui import Ui_MainWindow as DisplayResults_ui
from ..models.DisplayResultsModel import DisplayResultsModel
from ..controllers.DisplayResultsController import DisplayResultsController

progress_msgs = {
    0: 'Finish trim, start clean data',
    1: 'Finish clean data, start segment video',
    2: 'Finish segment video, start segment audio',
    3: 'Finish segment audio, start analyze audio',
    4: 'Finish analyze audio',
}


def log(msg: str) -> None:
    print(f'[DisplayResutls/View] {msg}')


class DisplayResultsView(QMainWindow, DisplayResults_ui):
    def __init__(self,
                 model: DisplayResultsModel,
                 controller: DisplayResultsController):
        super(DisplayResultsView, self).__init__()
        self._model = model
        self._controller = controller

        self.setupUi(self)
        self.create_threads()
        self.connect_to_controller()
        self.connect_to_model()
        self.set_default_values()

    def open(self):
        self.show()
        self.on_open()

    def close(self):
        self.hide()

    # region HELPER FUNCTIONS AND CALLBACKS

    def create_threads(self):
        self._controller.create_thread()

    def connect_to_controller(self):
        pass

    def connect_to_model(self):
        self._model.on_data_x_changed.connect(self.handle_data_x_changed)
        self._model.on_data_y_changed.connect(self.handle_data_y_changed)
        self._model.on_audio_data_changed.connect(
            self.handle_audio_data_changed)
        self._model.on_audio_fs_changed.connect(self.handle_audio_fs_changed)
        self._model.on_thread_status_update.connect(
            self.handle_update_status)
        self._model.on_image_changed.connect(self.display_image)

    def set_default_values(self):
        pass

    def on_open(self):
        try:
            self._controller.load_audio_file(
                ActualProjectModel.project_location)
            self._controller.load_frame_size(
                ActualProjectModel.project_location)
        except Exception as e:
            log(f'[ERROR] Error while loading audio file: {e}')

        if len(ActualProjectModel.data_x) == 0:
            # We are loading a project => so we need to:
            #  - Load Position Data
            #  - Load freq. range from .pro
            self._controller.load_position_data(
                ActualProjectModel.project_location)
        else:
            # We have to move data from 'ActualProjectModel' to the
            # DisplayResultsModel.
            self._controller.set_data_x(ActualProjectModel.data_x)
            self._controller.set_data_y(ActualProjectModel.data_y)
            self._controller.set_grid(ActualProjectModel.grid)

        self._controller.set_freq_range(
            [ActualProjectModel.low_freq, ActualProjectModel.high_freq])

        self._controller.load_bg_img(ActualProjectModel.project_location)

        self.pr_name.setText(ActualProjectModel.project_name)
        self.audio_info.setText(
            f'fs = {self._model.audio_fs}. ' +
            'Frequency Range: ' +
            f'{ActualProjectModel.low_freq}-{ActualProjectModel.high_freq}')
        self.grid_config.setText(str(self._model.grid))

    @Slot(np.ndarray)
    def handle_data_x_changed(self, value):
        log(f'Data: X -> length={len(value)}')

    @Slot(np.ndarray)
    def handle_data_y_changed(self, value):
        log(f'Data: Y -> length={len(value)}')

    def handle_audio_data_changed(self, value):
        log(f'Audio: data -> length={len(value)}')

    def handle_audio_fs_changed(self, value):
        log(f'Audio: fs -> {value}')

    @Slot(list)
    def handle_update_status(self, value: int) -> None:
        pass
        # total_grids = self._model.grid.number_of_cols * \
        #     self._model.grid.number_of_rows
        # log(f' *** Grid nº {value+1} of {total_grids}')
        # self.progressBar.setValue((value+1)/total_grids*100)

    @Slot(np.ndarray)
    def display_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.bg_img_label.setPixmap(qt_img)

        self._controller.start_thread()

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_format = QImage(
            rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qt_format)
