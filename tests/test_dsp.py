import os
import sys
import numpy as np
import time

from app.package.services import PyOctaveBand

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)


len_audio = 10**5
num_channels = 1

fs = 48000

times = []


for i in range(2):
    t = time.time()
    white_noise = np.random.rand(num_channels, len_audio) * 2 - 1
    spl, freq = PyOctaveBand.octavefilter(white_noise, fs, fraction=1)
    print(spl)
    times.append(time.time()-t)

# print(f'First time: {round(times[0], 3)}')
# print(f'Last time: {round(times[len(times)-1], 3)}')
print(f'Mean: {round(np.mean(times), 3)}')
