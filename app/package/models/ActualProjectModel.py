import numpy as np


class ActualProjectModel(object):
    """
        This class servers a Global Model.
        Others views should use their own Models to keep track of the data
        but when the user wants to actualy commit the changes, that Model
        should push its information here!
    """

    project_name = ''
    project_location = ''
    audio_device_index = -1
    video_device = -1
    low_freq = -1
    high_freq = -1
    time_of_rec = -1

    path_to_save = ''

    data_x = np.array([])
    data_y = np.array([])

    def __init__(self):
        super().__init__()
