__all__ = ['getTimeOfRecording']

from .PyOctaveBand import PyOctaveBand


def _getTime(B, e=0.1):
    #   e = 1 / (B*T)^(1/2)
    return 1/(B*e**2)


def _getSmallestBandwidth(low_freq, frac=3, fs=48000):
    freq, freq_d, freq_u = PyOctaveBand.genfreqs((low_freq, 10000), frac, fs)
    smallest_bandwidth = freq_u[0]-freq_d[0]

    return smallest_bandwidth


def getTimeOfRecording(lowest_freq, e=0.1, frac=3, fs=48000):
    sb = _getSmallestBandwidth(lowest_freq, frac, fs)

    return _getTime(sb, e)
