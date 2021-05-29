# This Python file uses the following encoding: utf-8
import numpy as np
import cv2

from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import Slot, QThread
from PySide2.QtWidgets import QMainWindow

from ..services.grid import Grid
from ..services import imbasic as imb
from ..services.DspThread import DspThread
from ..controllers.DisplayResultsController import DisplayResultsController
from ..models.ActualProjectModel import ActualProjectModel
from ..models.DisplayResultsModel import DisplayResultsModel
from ..ui.DisplayResults_ui import Ui_MainWindow as DisplayResults_ui

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib
from matplotlib import pyplot as plt

matplotlib.use('Qt5Agg')
plt.style.use('fivethirtyeight')

progress_msgs = {
    0: 'Finish trim, start clean data',
    1: 'Finish clean data, start segment video',
    2: 'Finish segment video, start segment audio',
    3: 'Finish segment audio, start analyze audio',
    4: 'Finish analyze audio',
}


def log(msg: str) -> None:
    print(f'[DisplayResutls/View] {msg}')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class DisplayResultsView(QMainWindow, DisplayResults_ui):
    def __init__(self,
                 model: DisplayResultsModel,
                 controller: DisplayResultsController):
        super(DisplayResultsView, self).__init__()
        self._model = model
        self._controller = controller

        self.setupUi(self)
        self.connect_to_controller()
        self.connect_to_model()
        self.set_default_values()

    def open(self):
        self.show()
        self.on_open()

    def close(self):
        self.hide()

    @staticmethod
    def log(msg: str) -> None:
        print(f'[DisplayResults/View] {msg}')

    # region HELPER FUNCTIONS AND CALLBACKS

    def setupPlottingWidget(self):
        sc = MplCanvas(self, width=5, height=4, dpi=100)

        # Show octave spectrum
        # sc.ax.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        sc.ax.grid(which='major')
        sc.ax.grid(which='minor', linestyle=':')
        sc.ax.set_xlabel(r'Frequency [Hz]')
        sc.ax.set_ylabel('Level [dB]')
        plt.xlim(11, 25000)

        # we save a reference to the widget, to then modify it
        self.sc = sc
        self.spectrum.addWidget(sc)

    def connect_to_controller(self):
        pass

    def connect_to_model(self):
        self._model.on_data_x_changed.connect(self.handle_data_x_changed)
        self._model.on_data_y_changed.connect(self.handle_data_y_changed)
        self._model.on_audio_data_changed.connect(
            self.handle_audio_data_changed)
        self._model.on_audio_fs_changed.connect(self.handle_audio_fs_changed)
        self._model.on_thread_status_update.connect(
            self.handle_update_status)
        self._model.on_image_changed.connect(self.display_image)
        self._model.on_row_changed.connect(self.handle_row_changed)
        self._model.on_col_changed.connect(self.handle_col_changed)
        self._model.on_grid_changed.connect(self.handle_grid_changed)

    def set_default_values(self):
        self.IMG_WIDTH = 350  # pixels
        self.scale_factor = -1

    def create_thread(self):
        # thread = QThread()
        # worker = AccountManager()
        # worker.moveToThread(thread)
        # thread.started.connect(lambda: worker.withdraw(person, amount))
        # worker.updatedBalance.connect(self.updateBalance)
        # worker.finished.connect(thread.quit)
        # worker.finished.connect(worker.deleteLater)
        # thread.finished.connect(thread.deleteLater)
        # return thread
        thread = QThread()
        worker = DspThread()
        worker.moveToThread(thread)

        thread.started.connect(lambda: worker.process(self._model))
        worker.update_status.connect(self.handle_update_status)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        return thread

    def on_open(self):
        self.setupPlottingWidget()

        try:
            self._controller.load_audio_file(
                ActualProjectModel.project_location)
            self._controller.load_frame_size(
                ActualProjectModel.project_location)
        except Exception as e:
            log(f'[ERROR] Error while loading audio file: {e}')

        if len(ActualProjectModel.data_x) == 0:
            # We are loading a project => so we need to:
            #  - Load Position Data
            #  - Load freq. range from .pro
            self._controller.load_position_data(
                ActualProjectModel.project_location)
        else:
            # We have to move data from 'ActualProjectModel' to the
            # DisplayResultsModel.
            self._controller.set_data_x(ActualProjectModel.data_x)
            self._controller.set_data_y(ActualProjectModel.data_y)
            self._controller.set_grid(ActualProjectModel.grid)

        self._controller.set_freq_range(
            [ActualProjectModel.low_freq, ActualProjectModel.high_freq])

        self._controller.load_bg_img(ActualProjectModel.project_location)

        self.pr_name.setText(ActualProjectModel.project_name)
        self.audio_info.setText(
            f'fs = {self._model.audio_fs}. ' +
            'Frequency Range: ' +
            f'{ActualProjectModel.low_freq}-{ActualProjectModel.high_freq}')
        self.grid_config.setText(str(self._model.grid))

        self.thread = self.create_thread()
        self.thread.start()

    # region Handlers

    @Slot(np.ndarray)
    def handle_data_x_changed(self, value):
        log(f'Data: X -> length={len(value)}')

    @Slot(np.ndarray)
    def handle_data_y_changed(self, value):
        log(f'Data: Y -> length={len(value)}')

    def handle_audio_data_changed(self, value):
        log(f'Audio: data -> length={len(value)}')

    def handle_audio_fs_changed(self, value):
        log(f'Audio: fs -> {value}')

    @Slot(Grid)
    def handle_grid_changed(self, grid: Grid) -> None:
        self.log(f'Setting maximum possible grid values: {grid}')

    @Slot(list)
    def handle_update_status(self, value: int) -> None:
        total_grids = self._model.grid.number_of_cols * \
            self._model.grid.number_of_rows
        self.log(f' *** Grid nº {value+1} of {total_grids}')
        # self.progressBar.setValue((value+1)/total_grids*100)

    @Slot(np.ndarray)
    def display_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        cv_img, scale_factor = imb.resize(cv_img, width=self.IMG_WIDTH,
                                          return_scale_factor=True)

        self.scale_factor = scale_factor

        qt_img = self.convert_cv_qt(cv_img)
        self.bg_img_label.setPixmap(qt_img)

        self.bg_img_label.mousePressEvent = self.handle_grid_clicked

    def handle_grid_clicked(self, event):
        """The (x,y) position of the event it is NOT in reference with
        the grid system. The coordinates must be scaled by a factor
        of 1/'self.scale_factor'
        See method 'display_image' for more info.

        Args:
            event ([type]): [description]
        """

        try:
            x = event.pos().x()
            y = event.pos().y()

            x, y = x/self.scale_factor, y/self.scale_factor

            grid_coord = self._model.grid.locate_point([x, y])

            # Check for hits in the padding zone (inside of the image, but
            # outside the grid system)
            if grid_coord is None:
                return

            self.log(f'Clicked on (x: {x} ,y: {y})')
            self.log(f'Corresponding to grid: {grid_coord}')

            self._controller.select_row(grid_coord[0])
            self._controller.select_col(grid_coord[1])
        except Exception as e:
            self.log(f'Error: {e}')

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_format = QImage(
            rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qt_format)

    @Slot(int)
    def handle_row_changed(self, value):
        if len(self._model.spectrum) == 0:
            return

        sp = self._model.spectrum[value, self._model.col]
        freq = self._model.freq

        print(sp, freq)

        if len(sp) == len(freq):
            self.redraw(freq, sp)
        else:
            self.log('Error len(sp) != len(freq)')

    @Slot(int)
    def handle_col_changed(self, value):
        if len(self._model.spectrum) == 0:
            return

        sp = self._model.spectrum[self._model.row, value]
        freq = self._model.freq

        print(sp, freq)

        if len(sp) == len(freq):
            self.redraw(freq, sp)
        else:
            self.log('Error len(sp) != len(freq)')

    def redraw(self, freq, spectrum):
        self.sc.ax.cla()  # Clear the canvas.

        xtick = [int(f) for f in freq]
        xticklabel = [str(round(f)) if f < 1000 else str(
            round(f/1000, 1))+'k' for f in freq]

        self.sc.ax.bar(freq, spectrum, width=np.array(freq)*2/5)

        self.sc.ax.set_xscale('log')
        self.sc.ax.set_xlabel(r'Frequency [Hz]')
        self.sc.ax.set_ylabel('Level [dB]')

        self.sc.ax.set_xticks(xtick)
        self.sc.ax.set_xticklabels(xticklabel)

        self.sc.draw()

    # endregion
