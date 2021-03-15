import sounddevice as sd

from PySide2.QtCore import QObject, Signal


class NewProjectModel(QObject):
    """
    The model class stores program data and state and some minimal logic for 
    announcing changes to this data
    """
    
    project_name_changed = Signal(str)
    project_location_changed = Signal(str)
    audio_driver_changed = Signal(int)
    audio_drivers_set = Signal(object)
    audio_device_changed = Signal(int)
    audio_devices_set = Signal(object)

    def __init__(self):
        super().__init__()
        self.clear_state()

    def clear_state(self):
        self._project_name = ''
        self._project_location = ''
        self._audio_drivers = ''
        self._audio_driver = ''
        self._audio_devices = ''
        self._audio_device = ''
        self._video_devices = ''
        self._video_device = ''
    
    @property
    def project_name(self):
        return self._project_name

    @project_name.setter
    def project_name(self, value):
        # print('[MODEL] cambiando project name')
        self._project_name = value
        self.project_name_changed.emit(value)
            
    @property
    def project_location(self):
        return self._project_location

    @project_location.setter
    def project_location(self, value):
        # print('[MODEL] cambiando project location')
        self._project_location = value
        self.project_location_changed.emit(value)

    @property
    def audio_drivers(self):
        return self._audio_drivers
    
    @audio_drivers.setter
    def audio_drivers(self, value):
        self._audio_drivers = value
        self.audio_drivers_set.emit(value)
        
    @property
    def audio_driver(self):
        return self._audio_driver

    @audio_driver.setter
    def audio_driver(self, value):
        # print(f'[MODEL] cambiando audio driver index: {value}')
        self._audio_driver = value
        self.audio_driver_changed.emit(value)
        
    @property
    def audio_devices(self):
        return self._audio_devices
    
    @audio_devices.setter
    def audio_devices(self, value):
        self._audio_devices = value
        self.audio_devices_set.emit(value)
        
    @property
    def audio_device(self):
        return self._audio_device

    @audio_device.setter
    def audio_device(self, value):
        # print(f'[MODEL] cambiando audio driver index: {value}')
        self._audio_device = value
        self.audio_device_changed.emit(value)
