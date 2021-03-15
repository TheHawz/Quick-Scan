import sounddevice as sd

from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import QFileDialog


class NewProjectController(QObject):

    navigator = Signal(str)

    def __init__(self, model):
        super().__init__()
        self._model = model

    @Slot(str)
    def navigate(self, value):
        self.navigator.emit(value)

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
        self._model.audio_device = value
        
    def set_audio_drivers(self):
        hostapis = sd.query_hostapis()
        drivers = [hostapi['name'] for hostapi in hostapis]
        self._model.audio_drivers = drivers
        
    def set_audio_devices(self, driver):
        print('setting audio devices')
        all_devices = sd.query_devices()
        devices = []
        for device in all_devices:
            if (device['hostapi'] == driver):
                if (device['max_input_channels'] > 0):
                    devices.append(device['name'])
                    
        self._model.audio_devices = devices
