import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os
from time import time

from PySide2.QtWidgets import QApplication, QFileDialog

import tempfile

# Config
t = 2  # s
fs = 44100


def save(x, fs):
    # You have to create a QApp in order to use a
    # Widget (QFileDialg)
    app = QApplication([])

    fname, _ = QFileDialog.getSaveFileName(
        None,
        caption='Save audio to disk',
        dir='C:/users/pablo/tfg',
        filter='Audio Wav File (.wav)')

    if fname == '':
        return

    if not fname.endswith('.wav'):
        fname += '.wav'

    write(fname, fs, x)


def main():
    with tempfile.TemporaryDirectory() as dir:
        # Rec
        print('Rec!')
        audio = sd.rec(frames=int(t*fs), samplerate=fs, channels=2)
        sd.wait()
        print('End!')

        # Sum to mono
        audio_mono = np.sum(audio, axis=1)

        # Calculate dB
        spl = 20 * np.log10(np.std(audio_mono) / 2e-5)
        print(round(spl, 2))

        path = os.path.join(dir, repr(time())+'.wav')
        write(path, 44100, audio_mono)

        r = input('Do you want to save it? [y]/n: ')
        if r == '' or r == 'y':
            save(audio_mono, fs)

    print('Ciao')


if __name__ == '__main__':
    main()
