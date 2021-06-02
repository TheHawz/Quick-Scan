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


def get_num_of_windows_2(len_audio, win_size, overlap):
    """Calculate the number of windows of size Ws that fit into an
    audio signal of length L with an overlap in a range of [0, 1).

    The while loop that can do this without knowing in advance the
    number of windows is the following:

    while i+win_size < len_audio:
        num_of_win += 1
        i += round(win_size-win_size*overlap)

    So we can deduce N from this inequations:
     -> L <= 0 + N*Ws - N*round(Ws*overlap) + Ws
     -> L <= N(Ws - round(Ws*overlap)) + Ws
     -> N >= L / (2*Ws - round(Ws+overlap))

    Args:
        len_audio (int):
            The longitude, in samples, of the audio signal.
        win_size (int):
            The longitude, in samples, of the window.
        overlap (float):
            The overlap between one window and the next, defined
            over a range of [0, 1)

    Returns:
        N (int):
            The number of windows, or in other words, the
            rows that we have to pre-allocate or the size
            of the loop that will iterate over it.
    """

    N = (len_audio-win_size) / (win_size - round(win_size*overlap))
    return int(np.ceil(N))


def get_spectrum(audio: np.ndarray, fs, limits=None):
    # make mono...
    audio = audio[0]

    win_type = 'square'
    win_size = 2**15
    overlap = 0.1
    len_audio = audio.shape[0]
    fraction = 3

    i = 0
    index = 0

    freq, _, _ = PyOctaveBand._genfreqs(limits, fraction, fs)
    num_of_win = get_num_of_windows(len_audio, win_size, overlap)
    spls = np.zeros([num_of_win, len(freq)])

    # print(f'len_audio = {len_audio}')
    # print(f'num_of_win = {num_of_win}')

    while i+win_size < len_audio:
        # if index % 50 == 0:
        #     print(f'Progres: {index} / {num_of_win}...')

        start = i
        end = i+win_size

        if win_type == 'square':
            audio_windowed = audio[start:end]

        _spl, _ = PyOctaveBand.octavefilter(
            audio_windowed, fs, fraction, 6, limits, False)

        spls[index] = _spl

        index += 1
        i += round(win_size-win_size*overlap)

    # print(f'max index: {index}')

    spl = np.mean(spls, 0)

    return spl, freq
