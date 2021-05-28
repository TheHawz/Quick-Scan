from app.package.services.DspThread import DspThread
import os
import numpy as np
import cv2
from scipy.io import wavfile

from PySide2.QtCore import QObject, Slot
from ..services import file as fileutils
from ..services.grid import Grid

from app.package.models.DisplayResultsModel import DisplayResultsModel


def log(msg):
    print(f'[Display Results] {msg}')


class DisplayResultsController(QObject):

    def __init__(self, model: DisplayResultsModel, navigator):
        super().__init__()
        self._model = model
        self._navigator = navigator

    @Slot(str)
    def navigate(self, value):
        self._navigator.navigator.emit(value)

    def create_thread(self):
        if self._model.dsp_thread is None:
            self._model.dsp_thread = DspThread(self._model)

    @Slot()
    def start_thread(self):
        self._model.dsp_thread = DspThread(self._model)
        self._model.dsp_thread.start()

    @Slot(np.ndarray)
    def set_data_x(self, value):
        self._model.data_x = value

    @Slot(np.ndarray)
    def set_data_y(self, value):
        self._model.data_y = value

    @Slot(list)
    def set_freq_range(self, value):
        self._model.freq_range = value

    @Slot()
    def set_grid(self, grid_info):
        self._model.grid = Grid(self._model.frame_size,
                                int(grid_info[0]), int(grid_info[1]),
                                int(grid_info[2]))

    # region LOADERS

    def load_audio_file(self, project_path: str) -> None:
        log('Loading audio file...')
        file_path = os.path.join(project_path,
                                 'Audio Files', 'audio.wav')
        exists, isFile = fileutils.check_for_existance(file_path)

        if not exists:
            raise Exception('File does not exist.')

        if not isFile:
            raise Exception('Path exists but is not a file.')

        fs, data = wavfile.read(file_path)
        self._model.audio_data = data
        self._model.audio_fs = fs

    def load_position_data(self, project_path: str) -> None:
        log('Loading position from file...')

        data_dir = os.path.join(project_path, 'Position Data')
        files_path = [os.path.join(data_dir, 'data.x'),
                      os.path.join(data_dir, 'data.y'),
                      os.path.join(data_dir, 'grid.config')]

        try:
            _x = np.loadtxt(files_path[0])
            _y = np.loadtxt(files_path[1])
            rows, cols, padding = np.loadtxt(files_path[2])

            if len(_x) == 0 or len(_y) == 0:
                raise FileNotFoundError('File is empty')

            self.set_data_x(_x)
            self.set_data_y(_y)
            self.set_grid([rows, cols, padding])

        except FileNotFoundError:
            raise Exception('File is empty')
        except Exception as e:
            raise Exception(f'Could not read position from files: {e}')

    def load_frame_size(self, project_path: str) -> None:
        log('Loading frame size from file...')

        data_dir = os.path.join(project_path, 'Position Data')
        files_path = os.path.join(data_dir, 'camera.data')

        try:
            width, height, fps = np.loadtxt(files_path)
            self._model.frame_size = [width, height]
            self._model.fps = fps
        except FileNotFoundError:
            raise Exception('File is empty')
        except Exception as e:
            raise Exception(f'Could not read frame size from file: {e}')

    def load_bg_img(self, project_path: str) -> None:
        data_dir = os.path.join(project_path, 'Images')
        files_path = os.path.join(data_dir, 'bg.png')

        try:
            img = cv2.imread(filename=files_path)
            if img is None:
                raise Exception('Image is empty.')

            print(f'*** Grid: {self._model.grid}')
            print(f'*** img.shape: {img.shape}')
            print(f'*** img.dtype: {img.dtype}')

            imgb = self._model.grid.draw_grid(img)
            self._model.image = imgb

        except FileNotFoundError:
            raise Exception('File is empty')
        except Exception as e:
            raise Exception(f'Unexpected error: {e}')

    # endregion
