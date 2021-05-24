from app.package.models.ActualProjectModel import ActualProjectModel
import os
from typing import Tuple
import numpy as np
from scipy.io import wavfile

from PySide2.QtCore import QObject, Slot
from ..services import file as fileutils
from ..services.grid import Grid
from ..services.path import interpolate_coords
from ..services import dsp

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

    @Slot(list)
    def set_freq_range(self, value):
        self._model.freq_range = value

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
        files_path = os.path.join(data_dir, 'camera.data')

        try:
            width, height, fps = np.loadtxt(files_path)
            self._model.frame_size = [width, height]
            self._model.fps = fps
        except FileNotFoundError:
            raise Exception('File is empty')
        except Exception as e:
            raise Exception(f'Could not frame size from files: {e}')

    # endregion

    # region DSP

    def dsp(self) -> None:
        log('### DSP ### ')

        trimmed_audio = self.trim_audio()
        shift, trim = self.clean_data_position()
        self._model.audio_data = trimmed_audio[shift:-trim]

        spatial_segmentation = self.segment_video()
        # for key in [*spatial_segmentation]:
        #     print(f'{key} -> {spatial_segmentation[key]}')

        audio_segments = self.segment_audio(spatial_segmentation)

        spectrum = self.analyze(audio_segments)
        print(spectrum)

    # region Helpers

    def trim_audio(self) -> np.ndarray:
        audio_len = len(self._model.audio_data)
        video_len = len(self._model.data_x)

        # TODO: get fps from camera
        fps = 30

        if (audio_len/self._model.audio_fs < video_len/fps):
            raise Exception('ERROR: Audio is shorter than needed...')

        max_audio_len = int(video_len * self._model.audio_fs / fps)

        log(f'Trimming the last {abs(audio_len-max_audio_len)} from audio')
        return self._model.audio_data[:max_audio_len]

    def clean_data_position(self) -> Tuple:
        if np.isnan(self._model.data_x).all():
            log('ERROR: There is no localization data to analyze')
            raise Exception('...')

        self._model.data_x, shift, trim = interpolate_coords(
            self._model.data_x)
        self._model.data_y, _, _ = interpolate_coords(self._model.data_y)

        return shift, trim

    def segment_video(self) -> dict[tuple, list[tuple]]:
        data = np.transpose(np.array([self._model.data_x, self._model.data_y]))

        grid = Grid(self._model.frame_size, NUMBER_OF_ROWS,
                    NUMBER_OF_COLS, PADDING)

        spatial_segmentation: dict[tuple, list[tuple]] = {}
        for i in range(NUMBER_OF_COLS):
            for j in range(NUMBER_OF_ROWS):
                spatial_segmentation[i, j] = []

        start = 0
        end = 0
        prev_grid_id = -1

        for index in range(len(data)):
            x, y = data[index]

            actual_grid_id = grid.locate_point((x, y))
            # np.array to python list
            actual_grid_id = [int(i) for i in actual_grid_id]

            if index == 1:
                prev_grid_id = actual_grid_id

            if prev_grid_id == actual_grid_id:
                end = index
            else:
                # spatial_segmentation[(start, end)] = actual_grid_id
                key = (actual_grid_id[0], actual_grid_id[1])
                spatial_segmentation[key].append((start, end))
                start = index
                end = index
                prev_grid_id = actual_grid_id

        return spatial_segmentation

    def segment_audio(self,
                      segmentation: dict[tuple, list[tuple]]
                      ) -> dict[tuple, list[tuple]]:
        # todo: get fps from camera
        fps = 30
        fs = self._model.audio_fs
        conversion_ratio = fs / fps

        audio_segments: dict[tuple, list[tuple]] = {}
        for grid_id in [*segmentation]:
            audio_segments[grid_id] = []

            for range in segmentation[grid_id]:
                start = int(range[0] * conversion_ratio)
                end = int(range[1] * conversion_ratio)
                audio_segment = self._model.audio_data[start:end]
                audio_segments[grid_id].extend(audio_segment)
                audio_segments[grid_id].extend(audio_segment)
                audio_segments[grid_id].extend(audio_segment)

        return audio_segments

    def analyze(self, audio_segments):
        spectrum = []
        for key in [*audio_segments]:
            audio = np.transpose(audio_segments[key])
            print(key)
            if len(audio) != 0:
                _spectrum = dsp.get_spectrum(audio, self._model.audio_fs)
                spectrum.append(_spectrum)

        fileutils.save_np_to_txt(spectrum, os.path.join(
            ActualProjectModel.project_location, 'Results'), 'results.spec')

        return spectrum

    # endregion

    # endregion
