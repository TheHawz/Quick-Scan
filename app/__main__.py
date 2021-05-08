# This Python file uses the following encoding: utf-8
from pstats import SortKey
import sys

from PySide2.QtWidgets import QApplication
from PySide2 import QtCore

from .package.models.NewProjectModel import NewProjectModel
from .package.models.DataAcquisitionModel import DataAcquisitionModel
from .package.models.DisplayResultsModel import DisplayResultsModel

from .package.controllers.Navigator import Navigator
from .package.controllers.NewProjectController import NewProjectController
from .package.controllers.DataAcquisitionController import DataAcquisitionController
from .package.controllers.DisplayResultsController import DisplayResultsController

from .package.views.MainWindow import MainWindow
from .package.views.NewProjectView import NewProjectView
from .package.views.DataAcquisitionView import DataAcquisitionView
from .package.views.DisplayResultsView import DisplayResultsView


class App(QApplication):

    # Diccionario que mapea nombres con Vistas
    views = {}

    def __init__(self):
        super(App, self).__init__()

        self.navigator = Navigator()
        self.navigator.navigator.connect(self.change_view)

        # MODELS
        self.new_project_model = NewProjectModel()
        self.data_acquisition_model = DataAcquisitionModel()
        self.display_results_model = DisplayResultsModel()

        # CONTROLLERS
        self.new_project_controller = NewProjectController(
            self.new_project_model, self.navigator)
        self.data_acquisition_controller = DataAcquisitionController(
            self.data_acquisition_model, self.navigator)
        self.display_results_controller = DisplayResultsController(
            self.display_results_model, self.navigator)

        # VIEWS
        self.main_view = MainWindow(None, self.navigator)
        self.new_project_view = NewProjectView(
            self.new_project_model, self.new_project_controller)
        self.data_acquisition_view = DataAcquisitionView(
            self.data_acquisition_model, self.data_acquisition_controller)
        self.display_results_view = DisplayResultsView(
            self.display_results_model, self.display_results_controller)

        App.views['main_view'] = self.main_view
        App.views['new_project'] = self.new_project_view
        App.views['data_acquisition'] = self.data_acquisition_view
        App.views['display_results'] = self.display_results_view

        self.change_view('new_project')

    @QtCore.Slot(str)
    def change_view(self, name_view, closeOthers=True):
        App.views.get(name_view).open()
        if not closeOthers:
            return
        for view in App.views:
            if view != name_view:
                self.views.get(view).close()


sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = App()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     import cProfile

#     cProfile.run('main()', 'output.dat')

#     import pstats
#     from pstats import SortKey

#     with open("output_time.dat", "w") as f:
#         p = pstats.Stats("output.dat", stream=f)
#         p.sort_stats("time").print_stats()

#     with open("output_calls.dat", "w") as f:
#         p = pstats.Stats("output.dat", stream=f)
#         p.sort_stats("calls").print_stats()
