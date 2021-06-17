from PyOctaveBand import octavefilter
import numpy as np

len_audio = 2**20
fs = 44100

x = np.random.rand(2, len_audio)*2-1
x = x.astype(np.float32)

amplitude = 0.5
x *= amplitude

# x = np.transpose(x)


def print_signal_info(x, name=''):
    print(f' - - - Signal {name} info - - - ')
    print(f'type: {type(x)}')
    print(f'length: {len(x)}')
    if type(x) == np.ndarray:
        print(f'dtype: {x.dtype}')
        print(f'shape: {x.shape}')
    print(f'max: {np.max(x)}')
    print(f'min: {np.max(x)}')


print_signal_info(x)


db, freq = octavefilter(x, fs, 3, 6, show=False)

print(np.round(freq).astype(int))
print(np.round(db).astype(int))
