# %%
# Imports
import numpy as np

import original as orig
import mine
from powerlawgaussian import powerlaw_psd_gaussian as gen_noise

len_audio = 2**20
num_channels = 2
fs = 44100

# %%

white_noise = np.random.rand(num_channels, len_audio)*2-1
pink_noise = gen_noise(1, [num_channels, len_audio])

# %%

_, _ = orig.octavefilter(white_noise, fs, 3, 6)
_, _ = mine.octavefilter(white_noise, fs, 3, 6)

# %%
