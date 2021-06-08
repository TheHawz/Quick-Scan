import os
import queue
import sys
from time import time

import sounddevice as sd
import soundfile as sf
from PySide2.QtCore import QObject, Signal

from ..models.ActualProjectModel import ActualProjectModel as actual_project
from . import file as fileutils


class MicWorker(QObject):
    update_volume = Signal(object)
    finished = Signal(bool)

    @staticmethod
    def log(msg):
        print(f'[MicWorker] {msg}')

    def config_mic(self, input_device, buffer=0):
        """[summary]

        Args:
            input_device ([type]): index of the actual input mic.
            fs (int, optional): Sampling frequency 44.1 kHz.
            buffer (int, optional): Defaults to 0 => automatic blocksize
        """
        self.io = (input_device, sd.default.device[1])
        self.fs = int(sd.query_devices()[input_device]['default_samplerate'])
        self.buffer = buffer
        self.q = queue.Queue()

        self._running = False
        self._rec = False

    def rec(self):
        self.log("Start recording!")
        self.start_time = time()
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

        if not self.error:
            elapsed = time()-self.start_time
            print(f' -> Time spent recording: {round(elapsed,2)}s')
            print(f' -> fs = {self.fs}')
            print(
                f' -> Theoretical num of samples => {round(elapsed*self.fs)}')

        self.finished.emit(self.error)

    def callback(self, indata, outdata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)

        # outdata[:] = indata
        # self.update_volume.emit(indata.copy())
        # print(indata)
        self.q.put(indata.copy())
