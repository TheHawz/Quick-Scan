import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os
from time import time

print('rec')
audio = sd.rec(frames=30*44100, samplerate=44100, channels=2)
sd.wait()
audio = np.array(audio)
print('stop')
path = os.path.join('rec', 'white_noise', 'lateral',
                    str(time())+'sin-bola.wav')
write(path, 44100, audio)
