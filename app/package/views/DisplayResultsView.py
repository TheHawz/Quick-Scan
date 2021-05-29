# This Python file uses the following encoding: utf-8
from ..services import imbasic as imb
from ..controllers.DisplayResultsController import DisplayResultsController
from ..models.DisplayResultsModel import DisplayResultsModel
from ..ui.DisplayResults_ui import Ui_MainWindow as DisplayResults_ui
from ..models.ActualProjectModel import ActualProjectModel
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QMainWindow
import numpy as np
import cv2

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
        self.setupPlottingWidget()
        self.create_threads()
        self.connect_to_controller()
        self.connect_to_model()
        self.set_default_values()

    def open(self):
        self.show()
        self.on_open()

    def close(self):
        self.hide()

    # region HELPER FUNCTIONS AND CALLBACKS

    def create_threads(self):
        self._controller.create_thread()

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
        self.row_sb.valueChanged.connect(self._controller.select_row)
        self.col_sb.valueChanged.connect(self._controller.select_col)

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

    def set_default_values(self):
        self.row_sb.setValue(1)
        self.col_sb.setValue(1)

    def on_open(self):
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

    @Slot(list)
    def handle_update_status(self, value: int) -> None:
        pass
        # total_grids = self._model.grid.number_of_cols * \
        #     self._model.grid.number_of_rows
        # log(f' *** Grid nº {value+1} of {total_grids}')
        # self.progressBar.setValue((value+1)/total_grids*100)

    @Slot(np.ndarray)
    def display_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        cv_img = imb.resize(cv_img, width=250)

        qt_img = self.convert_cv_qt(cv_img)
        self.bg_img_label.setPixmap(qt_img)

        self._controller.start_thread()

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

        sp = self._model.spectrum[value-1, self._model.col-1]
        freq = self._model.freq
        self.redraw(freq, sp)

    @Slot(int)
    def handle_col_changed(self, value):
        if len(self._model.spectrum) == 0:
            return

        sp = self._model.spectrum[self._model.row-1, value-1]
        freq = self._model.freq
        self.redraw(freq, sp)

    def redraw(self, freq, spectrum):
        self.sc.ax.cla()  # Clear the canvas.

        self.sc.ax.bar(freq, spectrum, width=[freq])

        self.sc.ax.grid(which='major')
        self.sc.ax.grid(which='minor', linestyle=':')
        self.sc.ax.set_xlabel(r'Frequency [Hz]')
        self.sc.ax.set_ylabel('Level [dB]')

        self.sc.draw()
