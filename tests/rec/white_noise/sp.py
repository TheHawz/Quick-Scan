# %%

# from scipy.fft import fft, fftshift
from scipy.fft import fft, fftshift
import numpy as np
from scipy import signal
from scipy.io.wavfile import read
from scipy.fft import fftshift
import matplotlib.pyplot as plt

files = ['frontal/1622536219.0725663sin-bola.wav',
         'frontal/1622536047.389629con-bola.wav']

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
win_type = 'square'
win_size = 2**15
overlap = 0.1
len_audio = x.shape[0]
fraction = 3

i = 0
index = 0

num_of_win = get_num_of_windows(len_audio, win_size, overlap)
window = signal.windows.hann(2**14)
# spls = np.zeros([num_of_win, len(x)])
spls = []

# print(f'len_audio = {len_audio}')
# print(f'num_of_win = {num_of_win}')

while i+win_size < len_audio:
    # if index % 50 == 0:
    #     print(f'Progres: {index} / {num_of_win}...')

    start = i
    end = i+win_size

    x_w = x[start:end]
    if win_type != 'square':
        x_w *= window

    freq = [1, 1, 1]
    _spl = [0, 0, 0]

    spls.append(_spl)

    index += 1
    i += round(win_size-win_size*overlap)


spl = np.mean(spls, 0)

fig = plt.Figure()
ax = fig.subplot()
ax.plot(freq, spl)
