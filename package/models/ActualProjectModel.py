from PySide2.QtCore import QObject, Signal


class ActualProjectModel(object):
    """
    This class servers a Global Model.
    Others views should use their own Models to keep track of the data
    but when the user wants to actualy commit the changes, that Model should
    push its information here!
    """

    project_name = ''
    project_location = ''
    audio_driver = -1
    audio_device = -1
    video_device = -1
    
    def __init__(self):
        super().__init__()
