from PySide2.QtCore import QObject


class CalibrateModel(QObject):
    def __init__(self):
        super().__init__()
        self.clear_state()

    def clear_state(self):
        pass
