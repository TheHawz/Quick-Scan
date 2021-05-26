__all__ = ['getTimeOfRecording']

from . import PyOctaveBand
import numpy as np


def _getTime(B, e=0.1):
    #   e = 1 / (B*T)^(1/2)
    return 1/(B*e**2)


def _getSmallestBandwidth(low_freq, frac=3, fs=48000):
    freq, freq_d, freq_u = PyOctaveBand._genfreqs((low_freq, 10000), frac, fs)
    smallest_bandwidth = freq_u[0]-freq_d[0]

    return smallest_bandwidth


def getTimeOfRecording(lowest_freq, e=0.1, frac=3, fs=48000):
    sb = _getSmallestBandwidth(lowest_freq, frac, fs)
    return _getTime(sb, e)


def get_num_of_windows(len_audio, win_size, overlap):
    i = 0
    num_of_win = 0

    while i+win_size < len_audio:
        num_of_win += 1
        i += round(win_size-win_size*overlap)

    return num_of_win


def get_spectrum(audio: np.ndarray, fs, limits=None):
    # make mono...
    audio = audio[0]

    win_type = 'square'
    win_size = 2**13
    overlap = 0.2
    len_audio = audio.shape[0]
    fraction = 1

    i = 0
    index = 0

    freq, _, _ = PyOctaveBand._genfreqs(limits, fraction, fs)
    num_of_win = get_num_of_windows(len_audio, win_size, overlap)
    spls = np.zeros([num_of_win, len(freq)])
    freqs = []

    print(f'len_audio = {len_audio}')
    print(f'num_of_win = {num_of_win}')

    while i+win_size < len_audio:
        if index % 50 == 0:
            print(f'{index} / {num_of_win}')

        start = i
        end = i+win_size

        if win_type == 'square':
            audio_windowed = audio[start:end]

        _spl, _freq = PyOctaveBand.octavefilter(
            audio_windowed, fs, fraction, 6, limits, False)
        freqs = _freq

        spls[index] = _spl

        index += 1
        i += round(win_size-win_size*overlap)

    print(f'max index: {index}')

    spl = np.mean(spls, 0)

    return spl, freqs
