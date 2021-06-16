# This Python file uses the following encoding: utf-8
import numpy as np
import cv2
import os

from PySide2.QtGui import QImage, QPixmap, QResizeEvent
from PySide2.QtCore import Slot, QThread
from PySide2.QtWidgets import QMainWindow, QProgressBar, QStatusBar

from ..services.grid import Grid
from ..services import imbasic as imb
from ..services.DspThread import DspThread
from ..controllers.DisplayResultsController import DisplayResultsController
from ..models.ActualProjectModel import ActualProjectModel
from ..models.DisplayResultsModel import DisplayResultsModel
from ..ui.DisplayResults_ui import Ui_MainWindow as DisplayResults_ui
from app.package.services.load_project import LoadFilesWorker

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

matplotlib.use('Qt5Agg')
plt.style.use(os.path.join('app', 'package', 'stylesheet.mplstyle'))


def freq_to_str(f) -> str:
    if f < 1000:
        return str(round(f))
    else:
        return str(round(f/1000, 1))+'k'


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None):
        self.fig = Figure(tight_layout=True)
        self.ax = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


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

        self.bg_img_label.resizeEvent = self.onResize

        # self.actionOpen_Project.triggered.connect(
        # self._controller._navigator.navigate('new_project'))

    def close(self):
        self.hide()

    @staticmethod
    def log(msg: str) -> None:
        print(f'[DisplayResults/View] {msg}')

    # region HELPER FUNCTIONS AND CALLBACKS

    def setupPlottingWidget(self):
        sc = MplCanvas(self)

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
        self.freq_cb.currentIndexChanged.connect(self.handle_octave_change)

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
        self._model.on_freq_changed.connect(self.handle_center_freq)
        self._model.on_full_band_spec_changed.connect(
            self.handle_full_band_spec_changed)
        self._model.on_spectrum_changed.connect(self.handle_spectrum_changed)

    def set_default_values(self):
        self.img = None
        self.IMG_WIDTH = 350  # pixels
        self.scale_factor = -1
        self.active_row, self.active_col = None, None
        self.max_db, self.min_db = 0, 100
        self.active_spl = None
        self.spl_bar = None

    # region Create Threads

    def create_thread(self):
        # Create worker and thread
        thread = QThread()
        worker = DspThread()
        worker.moveToThread(thread)

        # Conect the 'started' signal of the Thread
        # to the corresponding function in the worker
        thread.started.connect(lambda: worker.process(self._model))
        thread.started.connect(self.start_dsp)
        worker.update_status.connect(self.handle_update_status)

        # Connect the finished signal of thread & worker
        # with the corresponding stuff
        worker.finished.connect(lambda: self._controller.select_row(0))
        worker.finished.connect(lambda: self._controller.select_col(0))
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self.stop_dsp)
        return thread

    def create_loading_thread(self):
        # Create worker and thread
        thread = QThread()
        worker = LoadFilesWorker()
        worker.moveToThread(thread)

        # Conect the 'started' signal of the Thread
        # to the corresponding function in the worker
        thread.started.connect(lambda: worker.load(self._model))
        thread.started.connect(self.start_loading)
        worker.send_data.connect(self._controller.set_data)
        worker.send_grid.connect(self._controller.set_grid)
        worker.send_freq_range.connect(self._controller.set_freq_range)

        # Connect the finished signal of thread & worker
        # with the corresponding stuff
        worker.finished.connect(thread.quit)
        worker.finished.connect(self.show_project_info)
        worker.finished.connect(worker.deleteLater)

        thread.finished.connect(self.dsp_thread.start)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self.stop_loading)

        return thread

    def start_dsp(self):
        print('---------------------------- HEY')

    def stop_dsp(self):
        self.statusbar.removeWidget(self.pbar)

    def start_loading(self):
        # self.statusBar = QStatusBar()
        self.pbar = QProgressBar(self)
        self.statusbar.addWidget(self.pbar)

    def stop_loading(self):
        print('---------------------------- HEY2')

    # endregion

    def on_open(self):
        self.setupPlottingWidget()

        self.dsp_thread = self.create_thread()
        self.loading_thread = self.create_loading_thread()

        self.loading_thread.start()

    def show_project_info(self):
        self.pr_name.setText(ActualProjectModel.project_name)

        self.audio_info.setText(
            f'fs = {self._model.audio_fs}. ' +
            'Frequency Range: ' +
            f'{ActualProjectModel.low_freq}-{ActualProjectModel.high_freq}')

        self.grid_config.setText(str(self._model.grid))

    # region Handlers
    @Slot(np.ndarray)
    def handle_data_x_changed(self, value: np.ndarray):
        pass

    @Slot(np.ndarray)
    def handle_data_y_changed(self, value: np.ndarray):
        pass

    @Slot(list)
    def handle_audio_data_changed(self, value: list):
        pass

    @Slot(int)
    def handle_audio_fs_changed(self, value: int):
        pass

    @Slot(Grid)
    def handle_grid_changed(self, grid: Grid) -> None:
        self.num_of_cells = grid.number_of_cols * \
            grid.number_of_rows

    @Slot(list)
    def handle_update_status(self, value: int) -> None:
        # self.progressBar.setValue((value+1)/total_grids*100)
        self.log(f' *** Grid nº {value+1} of {self.num_of_cells}')
        self.pbar.setValue(int((value+1)/self.num_of_cells*100))

    @Slot(np.ndarray)
    def display_image(self, cv_img: np.ndarray):
        """Updates the image_label with a new opencv image"""
        if cv_img is None:
            return
        self.img = cv_img.copy()
        cv_img = self._model.grid.draw_grid(cv_img)

        cv_img = self.draw_map(cv_img)

        if self.active_col is not None:
            pt1, pt2 = self._model.grid.get_region([self.active_row,
                                                    self.active_col])
            cv_img = imb.draw_border(cv_img, pt1, pt2,
                                     color=(255, 255, 0),
                                     thickness=4)

        cv_img, self.scale_factor = imb.resize(cv_img, width=self.IMG_WIDTH,
                                               return_scale_factor=True)

        qt_img = self.convert_cv_qt(cv_img)
        self.bg_img_label.setPixmap(qt_img)

        self.bg_img_label.mousePressEvent = self.handle_grid_clicked

    @staticmethod
    def create_color_map(color0=(255, 0, 0), color1=(0, 0, 255)):
        LUT = np.linspace(color0, color1, 100, dtype=np.uint8)
        return LUT

    def draw_map(self, img):
        if self.active_spl is None:
            return img

        spl = self.active_spl
        spl = np.array(spl, dtype=int)
        min = self.min_db
        max = self.max_db
        lut = self.create_color_map()

        for irow, row in enumerate(spl):
            for icol, value in enumerate(row):
                pt1, pt2 = self._model.grid.get_region([irow, icol])

                index = int((value-min)*len(lut) / (max-min)) - 1
                img = imb.draw_filled_rectangle(img,
                                                pt1, pt2,
                                                lut[index],
                                                0.6)
        return img

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

        self.active_row = value

        # sp = self._model.spectrum[value, self._model.col]
        # freq = self._model.freq

        # if len(sp) == len(freq):
        # self.redraw(freq, sp)
        # else:
        # self.log('Error len(sp) != len(freq)')

    @Slot(int)
    def handle_col_changed(self, value):
        if len(self._model.spectrum) == 0:
            return

        self.active_col = value
        self.display_image(self.img)

        sp = self._model.spectrum[self._model.row, value]
        freq = self._model.freq

        if len(sp) == len(freq):
            self.redraw(freq, sp)
        else:
            self.log('Error len(sp) != len(freq)')

    def redraw(self, freq, spectrum):
        # TODO: can improve performance => just change data on the axes

        if self.spl_bar is not None:
            for ii, val in enumerate(spectrum):
                self.spl_bar.patches[ii].set_height(val)
            # self.spl_bar.datavalues = spectrum
            self.sc.draw()
            return

        self.sc.ax.cla()  # Clear the canvas.

        self.spl_bar = self.sc.ax.bar(
            freq, spectrum, width=np.array(freq)*1/6)

        self.sc.ax.set_xscale('log')
        self.sc.ax.set_ylim(self.min_db, self.max_db)
        self.sc.ax.set_xlabel(r'Frequency [Hz]')
        self.sc.ax.set_ylabel('Level [dB]')

        ticks, labels = self.get_xticks(freq)
        self.sc.ax.set_xticks(ticks[0])
        self.sc.ax.set_xticklabels(labels[0])
        # self.sc.ax.set_xticks(ticks[-1], minor=True)
        # self.sc.ax.set_xticklabels(labels[-1], minor=True)

        self.sc.fig.set_tight_layout(True)
        self.sc.draw()

    def get_xticks(self, freq):
        freq = np.round(freq)
        major = []
        minor = []

        major_label = []
        minor_label = []

        for ii, f in enumerate(freq):
            if ii % 3 == 0:
                major.append(round(f))
                major_label.append(freq_to_str(f))
            else:
                minor.append(round(f))
                minor_label.append(freq_to_str(f))
        return (major, minor), (major_label, minor_label)

    @Slot(object)
    def handle_center_freq(self, freqs):
        self.freq_cb.clear()
        self.freq_cb.addItem('Full Spectrum')
        self.freq_cb.addItems(list(map(freq_to_str, freqs)))

    @Slot(object)
    def handle_full_band_spec_changed(self, value):
        self.active_spl = value

    @Slot(object)
    def handle_spectrum_changed(self, value):
        self.max_db = np.max(value) * 1.1
        self.min_db = np.min(value) * 0.9

    def handle_octave_change(self, index):
        if len(self._model.spectrum) == 0:
            return

        if index == 0:
            self.active_spl = self._model.full_band_spec
        else:
            self.active_spl = self._model.spectrum[:, :, index-1]

        self.display_image(self.img)

    def onResize(self, e: QResizeEvent):
        self.IMG_WIDTH = e.size().width()
        if self.img is not None:
            self.display_image(self.img)

    # endregion

    # endregion
