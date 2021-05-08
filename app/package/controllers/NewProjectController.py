import math
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
        
    #region Get Drivers

    def get_audio_drivers(self):
        """Initial setup => get all available audio drivers
        Select audio driver that have at least 1 device 
        with max_input_channels > 0
        
         * Types *
        
        hostapi: {
            name:string, 
            devices: int[], 
            defualt_input_device: int
            defualt_output_device: int
        }
        """
        hostapis = sd.query_hostapis()
        all_devices = sd.query_devices()
        filtered_hostapis = []
        
        for hostapi in hostapis:
            devices_index = hostapi['devices']
            for index in devices_index:
                device = all_devices[index]
                if device['max_input_channels'] > 0:
                    filtered_hostapis.append(hostapi)
                    break
                    
        self._model.audio_drivers = filtered_hostapis
        return hostapis

    def set_audio_devices(self, driver):
        all_devices = sd.query_devices()
        actual_driver = self._model.audio_drivers[driver]
        actual_devices_index = actual_driver['devices']
        # default_device_index = actual_driver['defualt_input_device']
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

    def get_default_audio_device(self):
        input_device, _ = sd.default.device
        devices = sd.query_devices()
        return [devices[input_device]['hostapi'], input_device]
        
    #endregion
    
    @Slot(str)
    def change_project_name(self, value):
        self._model.project_name = value

    @Slot(str)
    def change_project_location(self, value):
        self._model.project_location = value

    @Slot(int)
    def change_audio_driver(self, index):
        self._model.audio_driver = index

    @Slot(int)
    def change_audio_device(self, value):
        self._model.audio_device = self._model.audio_devices_index[value]

    @Slot(int)
    def change_video_device(self, value):
        self._model.video_device = value

    @Slot(int)
    def change_low_freq(self, value):
        self._model.low_freq = round(math.exp(value/10))

    @Slot(int)
    def change_high_freq(self, value):
        self._model.high_freq = round(math.exp(value/10))
