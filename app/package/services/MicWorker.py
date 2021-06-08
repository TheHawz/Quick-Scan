import os
import sys
import sounddevice as sd
import soundfile as sf
import queue

from PySide2.QtCore import QObject, Signal

from . import file as fileutils
from ..models.ActualProjectModel import ActualProjectModel as actual_project


class MicWorker(QObject):
    update_volume = Signal(object)
    finished = Signal(bool)

    @staticmethod
    def log(msg):
        print(f'[MicWorker] {msg}')

    def config_mic(self, input_device, fs=44100, buffer=1024):
        self.io = (input_device, sd.default.device[1])
        self.fs = fs
        self.buffer = buffer
        self.q = queue.Queue()

        self._running = False
        self._rec = False

    def rec(self):
        self.log("Start recording!")
        self._rec = True

    def stop_rec(self):
        self.log("Stopping rec...")
        self._rec = False
        self._running = False

    def stop(self):
        self.error = True
        self._running = False  # to raise the Exception

    def run(self):
        self.error = False

        self.log("Running!")
        self._running = True

        self.stream = sd.Stream(device=self.io,
                                channels=2,
                                samplerate=self.fs,
                                blocksize=self.buffer,
                                callback=self.callback)

        path = os.path.join(actual_project.project_location, 'Audio Files')
        fileutils.mkdir(path)

        self.file_stream = sf.SoundFile(os.path.join(path, 'audio.wav'),
                                        mode='w',
                                        samplerate=self.fs,
                                        channels=2)
        try:
            with self.file_stream as file:
                with self.stream:
                    while self._running:
                        if self._rec:
                            file.write(self.q.get())
                        else:
                            self.q.get()

                        if not self._running:
                            raise KeyboardInterrupt("Recording stopped!")

        except KeyboardInterrupt as e:
            self.log(e)
        except Exception as e:
            self.log("Unexpected Exception:", e)

        self.finished.emit(self.error)

    def callback(self, indata, outdata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)

        # outdata[:] = indata
        # self.update_volume.emit(indata.copy())
        # print(indata)
        self.q.put(indata.copy())
