import os
import numpy as np
import cv2
from scipy.io import wavfile

from PySide2.QtCore import QObject, Signal

from ..models.ActualProjectModel import ActualProjectModel
from ..models.DisplayResultsModel import DisplayResultsModel


from ..services import file as fileutils


class LoadFilesWorker(QObject):
    finished = Signal()

    send_data = Signal(tuple)
    send_grid = Signal(object)
    send_freq_range = Signal(list)

    @staticmethod
    def log(msg: str) -> None:
        print(f'[Load Project Worker] {msg}')

    def load(self, model: DisplayResultsModel):
        self.log('Running!')

        try:
            self.load_audio_file(
                ActualProjectModel.project_location, model)
            self.load_frame_size(
                ActualProjectModel.project_location, model)
        except Exception as e:
            self.log(f'[ERROR] Error while loading audio file: {e}')

        if len(ActualProjectModel.data_x) == 0:
            # We are loading a project => so we need to:
            #  - Load Position Data
            #  - Load freq. range from .pro
            self.load_position_data(
                ActualProjectModel.project_location)
        else:
            # We have to move data from 'ActualProjectModel' to the
            # DisplayResultsModel.
            self.send_data.emit((ActualProjectModel.data_x,
                                ActualProjectModel.data_y))
            self.send_grid.emit(ActualProjectModel.grid)

        self.send_freq_range.emit(
            [ActualProjectModel.low_freq, ActualProjectModel.high_freq])

        self.load_bg_img(ActualProjectModel.project_location, model)

        self.finished.emit()

    def load_audio_file(self, project_path: str, model: DisplayResultsModel):
        self.log('[Audio] Loading audio file...')
        file_path = os.path.join(project_path,
                                 'Audio Files', 'audio.wav')
        exists, isFile = fileutils.check_for_existance(file_path)

        if not exists:
            raise Exception('File does not exist.')

        if not isFile:
            raise Exception('Path exists but is not a file.')

        fs, data = wavfile.read(file_path)

        if not type(data) == np.ndarray:
            raise Exception('Empty file!')

        if (data.dtype == np.int16):
            data = data.astype(np.float32) / 2**(16-1)
        else:
            raise Exception('Wav file format error!')

        print(data.shape)

        self.log(f'[Audio] fs = {fs}')
        self.log(f'[Audio] l = {round(len(data)/fs,2)} s')

        model.audio_data = data
        model.audio_fs = fs

    def load_position_data(self, project_path: str):
        self.log('Loading position from file...')

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

            self.send_data.emit((_x, _y))
            self.send_grid.emit([rows, cols, padding])

        except FileNotFoundError:
            raise Exception('File is empty')
        except Exception as e:
            raise Exception(f'Could not read position from files: {e}')

    def load_frame_size(self, project_path: str, model: DisplayResultsModel):
        self.log('Loading frame size from file...')

        data_dir = os.path.join(project_path, 'Position Data')
        files_path = os.path.join(data_dir, 'camera.data')

        try:
            width, height, fps = np.loadtxt(files_path)
            model.frame_size = [width, height]
            model.fps = fps
        except FileNotFoundError:
            raise Exception('File is empty')
        except Exception as e:
            raise Exception(f'Could not read frame size from file: {e}')

    def load_bg_img(self, project_path: str, model: DisplayResultsModel):
        self.log('Loading image from file...')
        data_dir = os.path.join(project_path, 'Images')
        files_path = os.path.join(data_dir, 'bg.png')

        try:
            img = cv2.imread(filename=files_path)
            if img is None:
                raise Exception('Image is empty.')

            model.image = img

        except FileNotFoundError:
            raise Exception('File is empty')
        except Exception as e:
            raise Exception(f'Unexpected error: {e}')
