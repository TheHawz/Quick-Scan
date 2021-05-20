import os
import numpy as np
from scipy.io import wavfile

from PySide2.QtCore import QObject, Slot
from ..services import file as fileutils


class DisplayResultsController(QObject):

    def __init__(self, model, navigator):
        super().__init__()
        self._model = model
        self._navigator = navigator

    @Slot(str)
    def navigate(self, value):
        self._navigator.navigator.emit(value)

    @Slot(np.ndarray)
    def set_data_x(self, value):
        self._model.data_x = value

    @Slot(np.ndarray)
    def set_data_y(self, value):
        self._model.data_y = value

    def load_audio_file(self, file_path: str) -> None:
        exists, isFile = fileutils.check_for_existance(file_path)

        if not exists:
            raise Exception('File does not exist.')

        if not isFile:
            raise Exception('Path exists but is not a file.')

        fs, data = wavfile.read(file_path)
        self._model.audio_data = data
        self._model.audio_fs = fs

    def load_position_data(self, project_path: str) -> None:
        print('[Display Results] Loading position from file...')

        data_dir = os.path.join(project_path, 'Position Data')
        files_path = [os.path.join(data_dir, 'data_x.txt'),
                      os.path.join(data_dir, 'data_y.txt')]

        try:
            _x = np.loadtxt(files_path[0])
            _y = np.loadtxt(files_path[1])

            self.set_data_x(_x)
            self.set_data_y(_y)

        except Exception as e:
            raise Exception(f'Could not read position from files: {e}')
