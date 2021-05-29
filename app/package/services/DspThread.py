import os
import numpy as np

from PySide2.QtCore import QThread, Signal

from ..models.DisplayResultsModel import DisplayResultsModel
from ..models.ActualProjectModel import ActualProjectModel

from ..services import file as fileutils
from ..services.path import interpolate_coords
from ..services import dsp


class DspThread(QThread):
    on_update_status = Signal(int)
    on_finished = Signal()

    def __init__(self, model: DisplayResultsModel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model = model
        self.init_values()

    def init_values(self):
        self.trimmed_audio: np.ndarray = None

    @staticmethod
    def log(msg: str) -> None:
        print(f'[DSP Thread] {msg}')

    def run(self):
        """
            Callback function executed whenever someone starts the QThreat
            (thread.start())
        """
        self.log('Running!')

        self.trimmed_audio = self.trim_audio()
        shift, trim = self.clean_data_position()
        self._model.audio_data = self.trimmed_audio[shift:-trim]

        spatial_segmentation = self.segment_video()
        audio_segments = self.segment_audio(spatial_segmentation)

        freq, spec = self.analyze(audio_segments)
        self._model.spectrum = spec
        self._model.freq = freq

        self.on_finished.emit()

    def trim_audio(self) -> np.ndarray:
        audio_len = len(self._model.audio_data)
        video_len = len(self._model.data_x)
        fs = self._model.audio_fs
        fps = self._model.fps

        if (audio_len/fs < video_len/fps):
            # raise Exception('ERROR: Audio is shorter than needed...')
            self.log('Audio is shorter than needed. ' +
                     'Deleting the last position data')
            diff_in_samples = video_len / fps*fs - audio_len
            self.log(f'diff_in_audio_samples: {int(diff_in_samples)}')

            position_data_to_remove = int(diff_in_samples/fs*fps)+1
            self.log(f'position_data_to_remove: {position_data_to_remove}')

            self._model.data_x = self._model.data_x[:-position_data_to_remove]
            self._model.data_y = self._model.data_y[:-position_data_to_remove]

        max_audio_len = int(video_len * self._model.audio_fs / self._model.fps)

        self.log(f'Trimming the last {abs(audio_len-max_audio_len)} ' +
                 'samples from audio')

        return self._model.audio_data[:max_audio_len]

    def clean_data_position(self) -> tuple:
        if np.isnan(self._model.data_x).all():
            self.log('ERROR: There is no localization data to analyze')
            raise Exception('...')

        self._model.data_x, shift, trim = interpolate_coords(
            self._model.data_x)
        self._model.data_y, _, _ = interpolate_coords(self._model.data_y)

        return shift, trim

    def segment_video(self) -> dict[tuple, list[tuple]]:
        data = np.transpose(np.array([self._model.data_x, self._model.data_y]))

        spatial_segmentation: dict[tuple, list[tuple]] = {}
        for i in range(self._model.grid.number_of_cols):
            for j in range(self._model.grid.number_of_rows):
                spatial_segmentation[j, i] = []

        start = 0
        end = 0
        prev_grid_id = -1

        for index in range(len(data)):
            x, y = data[index]

            actual_grid_id = self._model.grid.locate_point((x, y))

            # TODO: fix this
            if actual_grid_id is None:
                # If the point was outside of the Grid itself (padding...).
                continue

            # np.array to python list
            actual_grid_id = [int(i) for i in actual_grid_id]

            if index == 1:
                prev_grid_id = actual_grid_id

            if prev_grid_id == actual_grid_id:
                end = index
            else:
                key = (actual_grid_id[0], actual_grid_id[1])
                spatial_segmentation[key].append((start, end))
                start = index
                end = index
                prev_grid_id = actual_grid_id

        return spatial_segmentation

    def segment_audio(self,
                      segmentation: dict[tuple, list[tuple]]
                      ) -> dict[tuple, list[tuple]]:
        fps = self._model.fps
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

        return audio_segments

    def analyze(self, audio_segments):
        cols = self._model.grid.number_of_cols
        rows = self._model.grid.number_of_rows
        # Spectrum is of shape = (rows, cols, 0)
        spectrum = [[[] for _ in range(cols)]
                    for _ in range(rows)]
        freq = []
        limits = self._model.freq_range
        fs = self._model.audio_fs

        self.log(f'Limits: {limits}')

        for index, key in enumerate([*audio_segments]):
            self.log(f'Processing grid: {key}')
            self._model.on_thread_status_update.emit(index)

            audio = np.transpose(audio_segments[key])

            if len(audio) == 0:
                continue

            _spl, _freq = dsp.get_spectrum(audio, fs, limits)
            freq = _freq
            spectrum[key[0]][key[1]] = _spl

        self.log(f'Freq array: {freq}')

        self.save(spectrum, freq)

        return np.array(freq), np.array(spectrum)

    def save(self, sp, freq):
        spectrum = []
        for row in sp:
            for col in row:
                print(col)
                # spectrum.append(col)

        fileutils.save_np_to_txt(spectrum, os.path.join(
            ActualProjectModel.project_location, 'Results'), 'results.spec')
        fileutils.save_np_to_txt(freq, os.path.join(
            ActualProjectModel.project_location, 'Results'), 'resutls.freq')
