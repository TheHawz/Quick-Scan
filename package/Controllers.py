from PySide2.QtCore import QObject, QFile, Signal, Slot


class MainController(QObject):

    navigator = Signal(str)

    def __init__(self, model):
        super().__init__()

        self._model = model

    @Slot(str)
    def navigate(self, value):
        # print(f'value: {value}')
        self.navigator.emit(value)
