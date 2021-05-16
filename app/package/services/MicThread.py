import os
import sys
import sounddevice as sd
import soundfile as sf
import queue

from PySide2.QtCore import QThread, Signal

from . import file as fileutils
from ..models.ActualProjectModel import ActualProjectModel as actual_project


class MicThread(QThread):
    update_volume = Signal(object)

    def __init__(self, rate=44100, chunksize=1024, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rate = rate
        self.chunksize = chunksize
        self.device = ""
        self.q = queue.Queue()
        self._running = False
        self._rec = False

    def toogleRec(self):
        if not self._rec:
            self._rec = True
            print("[MicThread.py] Start recording!")
        else:
            self._rec = False
            self._running = False
            print("[MicThread.py] Stop recording!")

    def run(self):
        self._running = True

        self.stream = sd.Stream(channels=2, callback=self.callback)
        path = os.path.join(actual_project.project_location, 'Audio Files')
        fileutils.mkdir(path)
        self.file_stream = sf.SoundFile(os.path.join(path, 'audio.wav'),
                                        mode='w',
                                        samplerate=44100,
                                        channels=2)
        try:
            with self.file_stream as file:
                with self.stream:
                    while self._running:
                        if self._rec:
                            file.write(self.q.get())
                        if not self._running:
                            raise KeyboardInterrupt("End of recording")

        except KeyboardInterrupt as e:
            print("[MicThread.py]", e)
        except Exception as e:
            print("[MicThread.py] Exception:", e)

    def stop(self):
        if not self._running:
            return

        print("[MicThread.py] Stopping audio stream")
        self._rec = False
        self._running = False
        self.wait()

    def callback(self, indata, outdata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        # print('.')
        outdata[:] = indata
        self.update_volume.emit(indata.copy())
        self.q.put(indata.copy())
