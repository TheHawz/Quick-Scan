from PySide2.QtCore import QObject, Signal, Slot


class Navigator(QObject):

    navigator = Signal(str)

    def __init__(self):
        super().__init__()

    @Slot(str)
    def navigate(self, value): 
        self.navigator.emit(value)
