from PySide2.QtCore import QObject, Signal


class NewProjectModel(QObject):
    """
    The model class stores program data and state and some minimal logic for 
    announcing changes to this data
    """
    
    project_name_changed = Signal(str)
    project_location_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.clear_state()

    def clear_state(self):
        self._project_name = ''
        self._project_location = ''
        self._audio_driver = ''
        self._audio_device = ''
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
