import sounddevice as sd

from PySide2.QtCore import QObject, Signal
from package.services.dsp import getTimeOfRecording


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
    video_devices_set = Signal(object)
    video_device_changed = Signal(int)
    low_freq_changed = Signal(int)
    high_freq_changed = Signal(int)
    low_freq_forced = Signal(int)
    high_freq_forced = Signal(int)
    minimum_time_changed = Signal(float)

    def __init__(self):
        super().__init__()
        self.clear_state()

    def clear_state(self):
        self._project_name = ''
        self._project_location = ''
        self._audio_drivers = []
        self._audio_driver = 0
        self._audio_devices = []
        self._audio_devices_index = []
        self._audio_device = 0
        self._video_devices = {}
        self._video_device = 0
        self._low_freq = 20
        self._high_freq = 20000

    @property
    def project_name(self):
        return self._project_name

    @project_name.setter
    def project_name(self, value):
        self._project_name = value
        self.project_name_changed.emit(value)

    @property
    def project_location(self):
        return self._project_location

    @project_location.setter
    def project_location(self, value):
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
        self._audio_device = value
        self.audio_device_changed.emit(value)

    @property
    def video_devices(self):
        return self._video_devices.values()

    @video_devices.setter
    def video_devices(self, value):
        self._video_devices = value
        self.video_devices_set.emit(value)

    @property
    def video_device(self):
        return self._video_device

    @video_device.setter
    def video_device(self, value):
        self._video_device = value
        self.video_device_changed.emit(value)

    @property
    def low_freq(self):
        return self._low_freq

    @low_freq.setter
    def low_freq(self, value):
        self._low_freq = value
        if value >= self._high_freq:
            self.high_freq_forced.emit(value)
        self.low_freq_changed.emit(value)
        self.minimum_time_changed.emit(getTimeOfRecording(value))

    @property
    def high_freq(self):
        return self._high_freq

    @high_freq.setter
    def high_freq(self, value):
        self._high_freq = value
        if value <= self._low_freq:
            self.low_freq_forced.emit(value)
        self.high_freq_changed.emit(value)
