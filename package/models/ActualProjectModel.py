from PySide2.QtCore import QObject, Signal


class ActualProjectModel(QObject):
    """
    This class servers a Global Model.
    Others views should use their own Models to keep track of the data
    but when the user wants to actualy commit the changes, that Model should
    push its information here!
    """
    
    project_name_changed = Signal(str)
    project_location_changed = Signal(str)
    audio_driver_changed = Signal(int)
    audio_device_changed = Signal(int)
    video_device_changed = Signal(int)

    project_name = ''
    project_location = ''
    audio_driver = -1
    audio_device = -1
    video_device = -1
    
    def __init__(self):
        super().__init__()

    # @property
    # def project_name(self):
    #     return self._project_name

    # @project_name.setter
    # def project_name(self, value):
    #     self._project_name = value
    #     self.project_name_changed.emit(value)

    # @property
    # def project_location(self):
    #     return self._project_location

    # @project_location.setter
    # def project_location(self, value):
    #     self._project_location = value
    #     self.project_location_changed.emit(value)
        
    # @property
    # def audio_driver(self):
    #     return self._audio_driver

    # @audio_driver.setter
    # def audio_driver(self, value):
    #     self._audio_driver = value
    #     self.audio_driver_changed.emit(value)

    # @property
    # def audio_device(self):
    #     return self._audio_device

    # @audio_device.setter
    # def audio_device(self, value):
    #     self._audio_device = value
    #     self.audio_device_changed.emit(value)

    # @property
    # def video_device(self):
    #     return self._video_device
    
    # @video_device.setter
    # def video_device(self, value):
    #     self._video_device = value
    #     self.video_device_changed.emit(value)
