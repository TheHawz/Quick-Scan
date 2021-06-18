# This Python file uses the following encoding: utf-8
import cv2
import numpy as np
from time import time

from PySide2.QtCore import QThread, Signal

from ..models.ActualProjectModel import ActualProjectModel

from .grid import Grid
from . import imbasic as imb
from .mask import get_mask, get_circles


def invert(x):
    if x != 0:
        return 1/x
    else:
        return 0


class CameraThread(QThread):
    update_frame = Signal(np.ndarray)
    on_stop_recording = Signal(object)
    on_camera_caracteristics_detected = Signal(tuple)
    on_handle_all_regions_rec = Signal()

    # Mic location estimation
    open_size = 3
    close_size = 23

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_values()

    def init_values(self):
        self.x_data = []
        self.y_data = []
        self.x = -1
        self.y = -1
        self.min_time_rec = -1
        self.rows = -1
        self.cols = -1
        self.padding = -1
        self.last_frame = None

    def set_min_time(self, time_of_rec):
        self.min_time_rec = time_of_rec

    def run(self):
        print('[CAM] Running!')
        self._running = True
        self._rec = False

        cap = self.setup_camera()

        self.times = None

        t1 = time()
        rec_frames = 0

        while self._running:
            ret, frame = cap.read()
            processed_frame = None

            if not ret:
                break

            if self._rec:
                if self.times is None:
                    # This code will only execute once!
                    # At the start of the recording process
                    t1 = time()
                    self.times = np.zeros((self.rows, self.cols))

                processed_frame = self.process_frame(frame)
                rec_frames += 1

            else:
                self._grid.config(self.rows, self.cols, pad=self.padding)
                processed_frame = self.bypass(frame)
                self.time = time()

            self.update_frame.emit(processed_frame)

        if rec_frames != 0:
            fps = 1/((time()-t1)/rec_frames)
            cam_setup = (self.frame_size[0], self.frame_size[1], fps)
            self.on_camera_caracteristics_detected.emit(cam_setup)

        if self.x_data is not None:
            location_data = {"x_data": self.x_data, "y_data": self.y_data}

        self.on_stop_recording.emit(location_data)
        cv2.destroyAllWindows()
        cap.release()

    def setup_camera(self):
        # Trying DSHOW driver
        cap = cv2.VideoCapture(ActualProjectModel.video_device + cv2.CAP_DSHOW)
        ret, _ = cap.read()
        if not ret:
            cap = cv2.VideoCapture(ActualProjectModel.video_device)

        # Indices 4 and 3 represent the Horizontal and Vertical size of
        # the frame. dtype = int performs a floor() underneath.
        self.frame_size = np.array([cap.get(4), cap.get(3)], dtype=int)

        self._grid = Grid(self.frame_size, self.rows,
                          self.cols, padding=self.padding)

        # _, frame = cap.read()
        # self.on_camera_caracteristics_detected.emit(
        # (frame.shape[0], frame.shape[1]))

        return cap

    def process_circles(self, frame, circles):
        """Appends data to the arrays and draws circles in the frame

           DOC: habrá un subarray de 'np.nan' al principio de cada x_data y
           y_data. De esta forma se tendrá sincronizado el momento en el
           que el micro se coloca en posición
        Args:
            frame (np.ndarray): Image in numpy format
            circles (np.ndarray): Circles in array format
        """

        if circles is None:
            self.x_data.append(np.nan)
            self.y_data.append(np.nan)
        else:
            circles = np.round(circles[0, :]).astype("int")

            x, y, r = circles[0]
            self.x_data.append(x)
            self.y_data.append(y)
            self.x = x
            self.y = y
            frame = cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            frame = cv2.rectangle(
                frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    def process_frame(self, frame):
        """Process each frame

        Args:
            frame ([type]): [description]

        Returns:
            [type]: [description]
        """
        # self._grid.draw_grid(frame)
        self.process_circles(frame,
                             get_circles(get_mask(frame,
                                                  openSize=1,
                                                  closeSize=25),
                                         dp=3,
                                         minDist=250))

        self.draw_rec_indicator(frame)

        color_frame = self.draw_color_display(frame, self.times, self._grid)

        delta = time() - self.time
        self.time = time()

        if self.x != -1 and self.y != -1:
            grid = self._grid.locate_point((self.x, self.y))
            if grid is not None:
                self.times[grid[0]][grid[1]] += delta
                imb.draw_text(frame, f'{grid[0], grid[1]}', 15, 15)

        return color_frame

    def draw_rec_indicator(self, frame):
        cv2.circle(
            frame, (self._grid.size_of_frame[1]-30, 30), 8, (0, 0, 255), -1)

    def draw_color_display(self, frame, times: np.ndarray, grid: Grid):
        alpha = np.clip(times/ActualProjectModel.time_of_rec, 0, 1)

        if (alpha == 1).all():
            self.on_handle_all_regions_rec.emit()

        for irow, row in enumerate(alpha):
            for icol, a in enumerate(row):
                pt1, pt2 = grid.get_region([irow, icol])
                self.draw_overlay(frame, a, pt1, pt2)

        return frame

    def draw_overlay(self, frame, t, pt1, pt2):
        if t < 0.5:
            # Degradado rojo -> transparente
            alpha = 0.5 - t
            imb.draw_filled_rectangle(
                frame, pt1, pt2, (0, 0, 255), alpha)

        else:
            # Degradado transparente -> verde
            alpha = t - 0.5
            imb.draw_filled_rectangle(
                frame, pt1, pt2, (255, 0, 0), alpha)

        return frame

    def bypass(self, frame):
        # TODO: quitar flip en prod.
        # frame = cv2.flip(frame, 1)

        self.last_frame = np.copy(frame)

        # self._grid.draw_grid(frame)
        return frame

    def rec(self):
        self._rec = True
        print("[CamThread] Start recording!")

    def stop_rec(self):
        self._rec = False
        self._running = False
        print("[CamThread] Stop recording!")

    def setRows(self, value):
        self.rows = value

    def setCols(self, value):
        self.cols = value

    def setPadding(self, value):
        self.padding = value

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._rec = False
        self._running = False
        self.wait()
