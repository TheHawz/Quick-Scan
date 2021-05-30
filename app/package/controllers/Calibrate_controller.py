
from app.package.controllers.Navigator import Navigator
from app.package.models.Calibrate_model import CalibrateModel
from PySide2.QtCore import QObject


class CalibrateController(QObject):
    def __init__(self, model: CalibrateModel, navigator: Navigator):
        super().__init__()
        self._model = model
        self._navigator = navigator
