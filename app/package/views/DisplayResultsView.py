# This Python file uses the following encoding: utf-8
import os
import numpy as np

from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import Slot

from ..models.ActualProjectModel import ActualProjectModel
from ..ui.DisplayResults_ui import Ui_MainWindow as DisplayResults_ui


class DisplayResultsView(QMainWindow, DisplayResults_ui):
    def __init__(self, model, controller):
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
        self._model.data_x_changed.connect(self.on_data_x_changed)
        self._model.data_y_changed.connect(self.on_data_y_changed)
        self._model.audio_data_changed.connect(self.on_audio_data_changed)
        self._model.audio_fs_changed.connect(self.on_audio_fs_changed)
        pass

    def set_default_values(self):
        pass

    def on_open(self):
        self._controller.set_data_x(ActualProjectModel.data_x)
        self._controller.set_data_y(ActualProjectModel.data_y)
        try:
            self._controller.load_audio_file(os.path.join(
                ActualProjectModel.project_location,
                'Audio Files',
                'audio.wav'))

        except Exception as e:
            print(f'[ERROR] Error while loading audio file: {e}')

    @Slot(np.ndarray)
    def on_data_x_changed(self, value):
        print(f'Data: X -> length={len(value)}')

    @Slot(np.ndarray)
    def on_data_y_changed(self, value):
        print(f'Data: Y -> length={len(value)}')

    def on_audio_data_changed(self, value):
        print(f'Audio: data -> length={len(value)}')

    def on_audio_fs_changed(self, value):
        print(f'Audio: fs -> {value}')
