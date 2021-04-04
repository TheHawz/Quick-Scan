import sounddevice as sd

from PySide2.QtCore import QObject, Slot
from PySide2 import QtMultimedia

from ..models.ActualProjectModel import ActualProjectModel


class NewProjectController(QObject):

    def __init__(self, model, navigator):
        super().__init__()
        self._model = model
        self._navigator = navigator

    def create_new_project(self):
        # Pushing info to ActualProject Global Model
        ActualProjectModel.project_name = self._model.project_name
        ActualProjectModel.project_location = self._model.project_location
        ActualProjectModel.audio_device_index = self._model.audio_device
        ActualProjectModel.video_device = self._model.video_device

        self._navigator.navigate('data_acquisition')

    @Slot(str)
    def change_project_name(self, value):
        self._model.project_name = value

    @Slot(str)
    def change_project_location(self, value):
        self._model.project_location = value

    @Slot(int)
    def change_audio_driver(self, value):
        self._model.audio_driver = value

    @Slot(int)
    def change_audio_device(self, value):
        self._model.audio_device = self._model.audio_devices_index[value]

    def set_audio_drivers(self):
        hostapis = sd.query_hostapis()
        self._model.audio_drivers = hostapis

    def set_audio_devices(self, driver):
        all_devices = sd.query_devices()
        actual_driver = self._model.audio_drivers[driver]
        actual_devices_index = actual_driver['devices']
        input_devices_index = []

        input_devices = []
        for i in actual_devices_index:
            device = all_devices[i]
            if (device['max_input_channels'] > 0):
                input_devices.append(device['name'])
                input_devices_index.append(i)

        self._model.audio_devices_index = input_devices_index
        self._model.audio_devices = input_devices

    def set_video_devices(self):
        cameras = QtMultimedia.QCameraInfo.availableCameras()
        video_devices = {}
        index = 0
        for cam in cameras:
            video_devices[index] = cam.description()
            index += 1

        self._model.video_devices = video_devices

    @Slot(int)
    def change_video_device(self, value):
        self._model.video_device = value
