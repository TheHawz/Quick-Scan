# %%

# from scipy.fft import fft, fftshift
import numpy as np
from scipy import signal
from scipy.io.wavfile import read
from scipy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt

files = ['tests/rec/white_noise/frontal/1622536219.0725663sin-bola.wav',
         'tests/rec/white_noise/frontal/1622536047.389629con-bola.wav']

fs, x = read(files[1])
x = np.transpose(x)
x = x[1]

x /= np.max(np.abs(x))

print('fs:', fs)
print('x.shape: ', x.shape)
print('min: ', np.min(x))
print('max: ', np.max(x))


# %%
def get_num_of_windows(len_audio, win_size, overlap):
    i = 0
    num_of_win = 0

    while i+win_size < len_audio:
        num_of_win += 1
        i += round(win_size-win_size*overlap)

    return num_of_win


# %%
def get_spectrum(win_size=2**8):
    win_type = 'hanning'
    overlap = 0.1
    len_audio = x.shape[0]
    fraction = 3

    i = 0
    index = 0

    window = signal.windows.hann(win_size)
    spls = []

    while i+win_size < len_audio:
        # Windowing the signal.
        start = i
        end = i+win_size
        x_w = x[start:end]
        if win_type != 'square':
            x_w *= window

        # Calculating the spectrum (rfft)
        yf = rfft(x_w)
        yf = 20*np.log10(abs(yf))
        xf = rfftfreq(win_size, 1 / fs)
        spls.append(yf)

        # Updating index
        index += 1
        i += round(win_size-win_size*overlap)

    # Apply mean to all of the SPLs
    spl = np.mean(spls, 0)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(xf, spl)
    ax.set_xscale('log')
    ax.set_xlim([20, 20e3])
    plt.show()


get_spectrum(win_size=2**10)
