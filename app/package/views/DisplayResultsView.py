# This Python file uses the following encoding: utf-8
import numpy as np

from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import Slot

from ..models.ActualProjectModel import ActualProjectModel
from ..ui.DisplayResults_ui import Ui_MainWindow as DisplayResults_ui
from ..models.DisplayResultsModel import DisplayResultsModel
from ..controllers.DisplayResultsController import DisplayResultsController


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
        self.connect_to_controller()
        self.connect_to_model()
        self.set_default_values()

    def open(self):
        self.show()
        self.on_open()

    def close(self):
        self.hide()

    # region HELPER FUNCTIONS AND CALLBACKS

    def connect_to_controller(self):
        pass

    def connect_to_model(self):
        self._model.on_data_x_changed.connect(self.handle_data_x_changed)
        self._model.on_data_y_changed.connect(self.handle_data_y_changed)
        self._model.on_audio_data_changed.connect(
            self.handle_audio_data_changed)
        self._model.on_audio_fs_changed.connect(self.handle_audio_fs_changed)

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

        self._controller.dsp()
        # try:
        #     self._controller.dsp()
        # except Exception as e:
        #     log(e)
        #     # TODO: show Error msg...

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
