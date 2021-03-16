import sounddevice as sd

from PySide2.QtCore import QObject, Signal


class DataAcquisitionModel(QObject):

    def __init__(self):
        super().__init__()
