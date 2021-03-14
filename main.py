# This Python file uses the following encoding: utf-8
import sys

from PySide2.QtWidgets import QApplication
from PySide2 import QtCore

from package.DataAcquisition import DataAcquisition
from package.Model import Model
from package.Controllers import MainController
from package.MainWindow import MainWindow


class App(QApplication):

    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        # Diccionario que mapea nombres con Vistas
        self._views = {}

        self.model = Model()
        
        self.main_controller = MainController(self.model)
        self.main_controller.navigator.connect(self.change_view)

        self.main_view = MainWindow(self.model, self.main_controller)
        self.second_view = DataAcquisition(self.model, self.main_controller)
        self._views['main_view'] = self.main_view
        self._views['second_view'] = self.second_view
        
        self.change_view('main_view')

    @QtCore.Slot(str)
    def change_view(self, name_view, closeOthers=True):
        self._views.get(name_view).open()
        
        if not closeOthers: return
        for view in self._views:
            if view != name_view:
                self._views.get(view).close()


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = App(sys.argv)
    sys.exit(app.exec_())
