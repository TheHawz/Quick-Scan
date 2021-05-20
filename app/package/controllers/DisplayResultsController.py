import os
import numpy as np
from scipy.io import wavfile

from PySide2.QtCore import QObject, Slot
from ..services import file as fileutils
from ..services.grid import Grid


# TODO: make configurable
# GRID DEFINITION
NUMBER_OF_ROWS = 4
NUMBER_OF_COLS = 4
PADDING = 100


def log(msg):
    print(f'[Display Results] {msg}')


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
                      os.path.join(data_dir, 'data.y')]

        try:
            _x = np.loadtxt(files_path[0])
            _y = np.loadtxt(files_path[1])

            if len(_x) == 0 or len(_y) == 0:
                raise FileNotFoundError('File is empty')

            self.set_data_x(_x)
            self.set_data_y(_y)

        except FileNotFoundError:
            raise Exception('File is empty')
        except Exception as e:
            raise Exception(f'Could not read position from files: {e}')

    def load_frame_size(self, project_path: str) -> None:
        log('Loading frame size from file...')

        data_dir = os.path.join(project_path, 'Position Data')
        files_path = os.path.join(data_dir, 'frame.size')

        try:
            self._model.frame_size = np.loadtxt(files_path)
        except FileNotFoundError:
            raise Exception('File is empty')
        except Exception as e:
            raise Exception(f'Could not frame size from files: {e}')

    # endregion

    # region DSP

    def dsp(self) -> None:
        log()

        trimmed_audio = self.trim_audio()
        log(f'Trimmed audio len: {len(trimmed_audio)}')

        spatial_segmentation = self.segment_video()
        log(spatial_segmentation)

    # region Helpers

    def trim_audio(self) -> np.ndarray:
        audio_len = len(self._model.audio_data)
        video_len = len(self._model.data_x)

        fps = 30
        max_audio_len = video_len * self._model.audio_fs / fps

        log(f'Trimming the last {abs(audio_len-max_audio_len)} from audio_data')
        return self._model.audio_data[:max_audio_len]

    def segment_video(self) -> dict:
        x_data = np.loadtxt(os.path.join('data', 'x_data.txt'))
        y_data = np.loadtxt(os.path.join('data', 'y_data.txt'))

        data = np.transpose(np.array([x_data, y_data]))

        grid = Grid(self._model.frame_size, NUMBER_OF_ROWS,
                    NUMBER_OF_COLS, padding=60)

        grid_list = []
        for x, y in data:
            grid_id = grid.locate_point((x, y))
            grid_id = [int(i) for i in grid_id]  # np.array to python list
            grid_list.append(grid_id)

        start = 0
        end = 0
        grid = grid_list[0]

        dictionary = {}

        for index in range(len(grid_list)):
            _grid = grid_list[index]

            if grid == _grid:
                end = index
            else:
                dictionary[(start, end)] = _grid
                start = index
                end = index
                grid = _grid

        return dictionary

    # endregion

    # endregion
