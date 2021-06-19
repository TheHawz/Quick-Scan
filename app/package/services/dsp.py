# -*- coding: utf-8 -*-
"""Module for digital signal processing related functions.

This module is needed for knowing the minimum time of recording per
region for the Scan&Paint method and to actualy get the spectrum
analysis for a single audio signal.
"""

from . import PyOctaveBand
import numpy as np
from scipy import signal


def _getTime(B, e=0.1):
    return 1/(B*e**2)


def _getSmallestBandwidth(low_freq, frac=3, fs=48000):
    _, freq_d, freq_u = PyOctaveBand._genfreqs((low_freq, 10000), frac, fs)
    smallest_bandwidth = freq_u[0]-freq_d[0]

    return smallest_bandwidth


def get_time_of_recording(lowest_freq, e=0.1, frac=3, fs=48000):
    """Function that returns the minimum time of recording for a
    given frequency range.

    There is an error related to analyzing random data signals, called
    the Normalized Random Error. If this error is less than 20 %, it can
    be approximated as a function of the bandwidth and the time of recording.

    If we perform a one third-octave spectrum analysis over a signal,
    the maximum error will be directly related to the bandwidth of the
    lowest band.

    Args:
        lowest_freq (float): The lowest frequency considered for the analysis
        e (float, optional): Maximum error tolerated. Defaults to 0.1.
        frac (int, optional): Fraction for the 1/x octave spectrum analysis. 
            Defaults to 3.
        fs (int, optional): Audio sampling frequency. Defaults to 48000.

    Returns:
        float: Minimum time of recording per area to analyze.
    """
    sb = _getSmallestBandwidth(lowest_freq, frac, fs)
    return _getTime(sb, e)


def _get_num_of_windows(len_audio, win_size, overlap):
    """returns the number of windows of size Ws that fit into an
    audio signal of length L with overlap.

    The while loop that can do this without knowing in advance the
    number of windows is the following:

    while i+win_size < len_audio:
        ...
        i += round(win_size-win_size*overlap)

    So we can deduce N from this inequations:
     -> L <= 0 + N * (Ws - round(Ws*overlap)) + Ws
     -> N >= (L-Ws) / (Ws - round(Ws+overlap))

    Args:
        len_audio (int):
            The longitude, in samples, of the audio signal.
        win_size (int):
            The longitude, in samples, of the window.
        overlap (float):
            The overlap between one window and the next, defined
            over a range of [0, 1)

    Returns:
        int: the number of windows
    """

    N = (len_audio-win_size) / (win_size - round(win_size*overlap))
    return int(np.ceil(N))


def get_spectrum(audio: np.ndarray,
                 fs: int,
                 limits=[12, 20000]
                 ) -> tuple[list, list]:
    """Function that returns one third-octave spectrum analysis of a signal

    It does so while windowing the signal with a Hannin window of size
    2^15 samples, with an overlap of 50%

    Args:
        audio (np.ndarray): Audio two-dimensional array. First dimension:
            number of channels. Second dimension: length of the audio
        fs (int): sampling rate
        limits (list, optional): Limits for the frequency
        spectrum analysis. Defaults to None.

    Returns:
        tuple[list, list]: Returns the spectrum values and the frequency array.
    """
    print(f'Get Spectrum. Audio.shape = {audio.shape}')

    win_size = 2**16
    overlap = 0.5
    len_audio = audio.shape[0]
    fraction = 3
    window = signal.windows.hann(win_size)

    i = 0
    index = 0

    freq, _, _ = PyOctaveBand._genfreqs(limits, fraction, fs)
    num_of_win = _get_num_of_windows(len_audio, win_size, overlap)
    spls = np.zeros([num_of_win, len(freq)])

    while i+win_size < len_audio:
        start, end = i, i+win_size

        audio_windowed = audio[start:end] * window

        _spl, f = PyOctaveBand.octavefilter(
            audio_windowed, fs, fraction, 6, limits, False)

        spls[index] = _spl

        index += 1
        i += round(win_size-win_size*overlap)

    spl = np.mean(spls, 0)
    return spl, freq
