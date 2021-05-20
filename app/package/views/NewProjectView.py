# This Python file uses the following encoding: utf-8
import math
import os

from PySide2.QtWidgets import QMainWindow, QFileDialog
from PySide2.QtCore import Slot

from ..ui.NewProject_ui import Ui_MainWindow as NewProject_ui


def freq_to_text(value: float) -> str:
    if value >= 1000:
        return f'{round(value/1000, 1)} kHz'

    return f'{round(value, 1)} Hz'


class NewProjectView(QMainWindow, NewProject_ui):

    def __init__(self, model, controller):
        super(NewProjectView, self).__init__()
        self._model = model
        self._controller = controller

        # self.load_ui()
        self.setupUi(self)
        self.connect_to_controller()
        self.connect_to_model()
        self.set_default_values()

    def open(self):
        self.show()

    def close(self):
        self.hide()

    def connect_to_controller(self):
        self.line_project_name.textChanged.connect(
            self._controller.change_project_name)
        self.line_project_location.textChanged.connect(
            self._controller.change_project_location)
        self.open_location.clicked.connect(self.open_location_dialog)
        self.cb_audio_driver.currentIndexChanged.connect(
            self._controller.change_audio_driver)
        self.cb_audio_device.currentIndexChanged.connect(
            self._controller.change_audio_device)
        self.but_create.clicked.connect(
            self._controller.create_new_project)
        self.cb_video_devices.currentIndexChanged.connect(
            self._controller.change_video_device)
        self.low_freq_dial.valueChanged.connect(
            self._controller.change_low_freq)
        self.high_freq_dial.valueChanged.connect(
            self._controller.change_high_freq)
        self.open_project_button.clicked.connect(self.open_project)

    def connect_to_model(self):
        self._model.project_name_changed.connect(self.project_name_changed)
        self._model.project_location_changed.connect(
            self.handle_project_location_changed)
        self._model.audio_drivers_set.connect(self.handle_audio_drivers_set)
        self._model.audio_driver_changed.connect(
            self.handle_audio_driver_changed)
        self._model.audio_devices_set.connect(self.handle_audio_devices_set)
        self._model.audio_device_changed.connect(
            self.handle_audio_device_changed)
        self._model.video_devices_set.connect(self.handle_video_devices_set)
        self._model.video_device_changed.connect(
            self.handle_video_device_changed)
        self._model.low_freq_changed.connect(self.handle_low_freq_changed)
        self._model.high_freq_changed.connect(self.handle_high_freq_changed)
        self._model.low_freq_forced.connect(self.handle_low_freq_forced)
        self._model.high_freq_forced.connect(self.handle_high_freq_forced)
        self._model.minimum_time_changed.connect(
            self.handle_minimum_time_changed)

    def set_default_values(self):
        self._controller.change_project_location(os.path.expanduser("~"))
        self._controller.change_project_name('New Project')

        self._controller.get_audio_drivers()
        self._controller.set_video_devices()
        self.high_freq_dial.setValue(1000)
        self.low_freq_dial.setValue(40)
        hostapi, device = self._controller.get_default_audio_device()
        self.cb_audio_driver.setCurrentIndex(hostapi)
        self.cb_audio_device.setCurrentIndex(device)

    def open_location_dialog(self):
        _dir = str(QFileDialog.getExistingDirectory(
            self, "Choose a location.", str(self._model.project_location)))
        if _dir != '':
            self._controller.change_project_location(_dir)

    @Slot()
    def open_project(self):
        fpath, _ = QFileDialog.getOpenFileName(self, "Open a project.", str(
            self._model.project_location), filter="Project files (*.pro)")
        if fpath != '':
            self._controller.load_new_project(fpath)

    # region SLOTS

    @Slot(str)
    def project_name_changed(self, value):
        self.line_project_name.setText(value)

    @Slot(str)
    def handle_project_location_changed(self, value):
        self.line_project_location.setText(value)

    @Slot(object)
    def handle_audio_drivers_set(self, value):
        # driver_names = [*value]  # Unpacking dict keys
        names = [v['name'] for v in value]
        self.cb_audio_driver.clear()
        self.cb_audio_driver.addItems(names)

    @Slot(int)
    def handle_audio_driver_changed(self, value):
        self._controller.set_audio_devices(value)

    @Slot(object)
    def handle_audio_devices_set(self, value):
        self.cb_audio_device.clear()
        self.cb_audio_device.addItems(value)

    @Slot(int)
    def handle_audio_device_changed(self, value):
        print(f'[VIEW]: Audio Device changed: {value}')

    @Slot(object)
    def handle_video_devices_set(self, value):
        self.cb_video_devices.clear()
        self.cb_video_devices.addItems(list(value.values()))

    @Slot(int)
    def handle_video_device_changed(self, value):
        print(f'[VIEW]: Video Device changed: {value}')

    @Slot(int)
    def handle_low_freq_changed(self, value):
        self.low_freq_label.setText(freq_to_text(value))

    @Slot(int)
    def handle_high_freq_changed(self, value):
        self.high_freq_label.setText(freq_to_text(value))

    @Slot(int)
    def handle_low_freq_forced(self, value):
        self.low_freq_dial.setValue(math.floor(math.log(value))*10-1)

    @Slot(int)
    def handle_high_freq_forced(self, value):
        self.high_freq_dial.setValue(math.ceil(math.log(value))*10+1)

    @Slot(float)
    def handle_minimum_time_changed(self, value):
        self.minimum_time_label.setText(
            f'Minimum time of recording:\n {round(value, 2)}s')
    # endregion
