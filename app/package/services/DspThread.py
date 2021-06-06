import os
import numpy as np

from PySide2.QtCore import QObject, Signal

from ..models.DisplayResultsModel import DisplayResultsModel
from ..models.ActualProjectModel import ActualProjectModel

from ..services import file as fileutils
from ..services.path import interpolate_coords
from ..services import dsp


class DspThread(QObject):
    update_status = Signal(int)
    finished = Signal()

    # def __init__(self, model: DisplayResultsModel, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     model = model
    #     self.init_values()

    # def init_values(self):
    #     self.trimmed_audio: np.ndarray = None

    @staticmethod
    def log(msg: str) -> None:
        print(f'[DSP Thread] {msg}')

    def process(self, model: DisplayResultsModel):

        self.log('Running!')

        self.trimmed_audio = self.trim_audio(model)
        shift, trim = self.clean_data_position(model)
        model.audio_data = self.trimmed_audio[shift:-trim]

        spatial_segmentation = self.segment_video(model)
        audio_segments = self.segment_audio(model, spatial_segmentation)

        model.freq, model.spectrum = self.analyze(model, audio_segments)
        model.full_band_spec = self.get_full_band(model, audio_segments)
        print(model.full_band_spec)
        self.finished.emit()

    def trim_audio(self, model) -> np.ndarray:
        audio_len = len(model.audio_data)
        video_len = len(model.data_x)
        fs = model.audio_fs
        fps = model.fps

        if (audio_len/fs < video_len/fps):
            # raise Exception('ERROR: Audio is shorter than needed...')
            self.log('Audio is shorter than needed. ' +
                     'Deleting the last position data')
            diff_in_samples = video_len / fps*fs - audio_len
            self.log(f'diff_in_audio_samples: {int(diff_in_samples)}')

            position_data_to_remove = int(diff_in_samples/fs*fps)+1
            self.log(f'position_data_to_remove: {position_data_to_remove}')

            model.data_x = model.data_x[:-position_data_to_remove]
            model.data_y = model.data_y[:-position_data_to_remove]

        max_audio_len = int(video_len * model.audio_fs / model.fps)

        self.log(f'Trimming the last {abs(audio_len-max_audio_len)} ' +
                 'samples from audio')

        return model.audio_data[:max_audio_len]

    def clean_data_position(self, model) -> tuple:
        if np.isnan(model.data_x).all():
            self.log('ERROR: There is no localization data to analyze')
            raise Exception('...')

        model.data_x, shift, trim = interpolate_coords(
            model.data_x)
        model.data_y, _, _ = interpolate_coords(model.data_y)

        return shift, trim

    @staticmethod
    def index_of_grid(data, id):
        ocurrences = []
        for index, d in enumerate(data):
            if d is None:
                continue
            if (id == d).all():
                ocurrences.append(index)

        return ocurrences

    @staticmethod
    def group_consecutives(array):
        if not len(array) > 0:
            return

        if len(array) == 1:
            return array*2

        ranges = []

        start = array[0]
        end = array[0]
        prev_int = -1

        for ii, value in enumerate(array):
            if ii == 0:
                prev_int = value
                continue

            if value == prev_int+1:
                end = value
                if ii == len(array)-1:
                    ranges.append([start, end])
            else:
                ranges.append([start, end])
                start = value
                end = value

            prev_int = value

        return ranges

    def segment_video(self,
                      model: DisplayResultsModel) -> dict[tuple, list[tuple]]:
        print('Segmenting video')
        data_pts = np.transpose([model.data_x, model.data_y])

        data_grids = np.array(
            list(map(model.grid.locate_point, data_pts)),
            dtype=object)

        cols = model.grid.number_of_cols
        rows = model.grid.number_of_rows

        grids = []
        for i in range(rows):
            for j in range(cols):
                grids.append([i, j])

        d = {}
        for id in grids:
            d[tuple(id)] = self.index_of_grid(data_grids, id)

        # print('SPATIAL SEGMENTATION: ')

        for key in [*d]:
            # print(f'Grid: {key}')
            cons = self.group_consecutives(d[key])
            d[key] = cons
            # print(cons)

        return d

    def segment_audio(self, model,
                      segmentation: dict[tuple, list[tuple]]
                      ) -> dict[tuple, list[tuple]]:
        fps = model.fps
        fs = model.audio_fs
        conversion_ratio = fs / fps

        audio_segments: dict[tuple, list[tuple]] = {}
        for grid_id in [*segmentation]:
            audio_segments[grid_id] = []

            for range in segmentation[grid_id]:
                start = int(range[0] * conversion_ratio)
                end = int((range[1]+1) * conversion_ratio)-1
                audio_segment = model.audio_data[start:end]
                audio_segments[grid_id].extend(audio_segment)

        return audio_segments

    def analyze(self, model, audio_segments):
        cols = model.grid.number_of_cols
        rows = model.grid.number_of_rows

        # Spectrum is of shape = (rows, cols, 0)
        spectrum = [[[] for _ in range(cols)]
                    for _ in range(rows)]
        freq = []
        limits = model.freq_range
        fs = model.audio_fs

        self.log(f'Limits: {limits}')

        for index, key in enumerate([*audio_segments]):
            self.log(f'Processing grid: {key}')
            self.update_status.emit(index)

            audio = np.transpose(audio_segments[key])

            if len(audio) == 0:
                self.log('Len audio == 0. Continuing...')
                continue

            _spl, _freq = dsp.get_spectrum(audio, fs, limits)
            freq = _freq
            spectrum[key[0]][key[1]] = _spl

        self.log(f'Freq array: {freq}')

        self.save(spectrum, freq)

        return np.array(freq), np.array(spectrum, dtype=object)

    def get_full_band(self, model, audio_segments):
        cols = model.grid.number_of_cols
        rows = model.grid.number_of_rows

        spectrum = [[0 for _ in range(cols)]
                    for _ in range(rows)]

        for key in [*audio_segments]:
            self.log(f'Processing grid: {key}')
            spl = 20 * np.log10(np.std(audio_segments[key]) / 2e-5)
            spectrum[key[0]][key[1]] = spl

        return spectrum

    def save(self, sp, freq):
        spectrum = []
        for row in sp:
            for col in row:
                spectrum.append(col)

        fileutils.save_np_to_txt(spectrum, os.path.join(
            ActualProjectModel.project_location, 'Results'), 'results.spec')
        fileutils.save_np_to_txt(freq, os.path.join(
            ActualProjectModel.project_location, 'Results'), 'resutls.freq')
