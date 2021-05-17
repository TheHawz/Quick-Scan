# This Python file uses the following encoding: utf-8
import cv2
import numpy as np
import time

from PySide2.QtCore import QThread, Signal

from ..models.ActualProjectModel import ActualProjectModel

# from ..services import colorSegmentation as cs  # Credits to Lara!
from .grid import Grid
from . import imbasic as imb
from .mask import get_mask, get_circles

# TODO: move to own file
# GRID DEFINITION
NUMBER_OF_ROWS = 4
NUMBER_OF_COLS = 4
PADDING = 100


class CameraThread(QThread):
    update_frame = Signal(np.ndarray)
    on_stop_recording = Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x_data = []
        self.y_data = []
        self.x = -1
        self.y = -1

    def run(self):
        """
            Callback function executed whenever someone starts the QThreat
            (thread.start())
        """
        print('[CAM] Running!')
        self._running = True
        self._rec = False

        cap = cv2.VideoCapture(ActualProjectModel.video_device + cv2.CAP_DSHOW)

        # Trying DSHOW driver
        frame, ret = cap.read()
        if not ret:
            cap = cv2.VideoCapture(ActualProjectModel.video_device)

        self.frame_size = np.array([int(cap.get(3)), int(cap.get(4))])
        self._grid = Grid(self.frame_size, NUMBER_OF_ROWS,
                          NUMBER_OF_COLS, padding=60)

        self.times = np.zeros((NUMBER_OF_ROWS, NUMBER_OF_COLS))
        self.time = time.time()

        while self._running:
            ret, frame = cap.read()

            if not ret:
                break

            processed_frame = None

            if not self._rec:
                self._grid.config(NUMBER_OF_ROWS, NUMBER_OF_COLS, pad=20)
                processed_frame = self.bypass(frame)
            else:
                processed_frame = self.process_frame(frame)

            self.update_frame.emit(processed_frame)

        # print('Stopping Camera Thread!')
        # print('*' * 40)
        # print('Times: \n', self.times)

        emit_obj = {"x_data": self.x_data, "y_data": self.y_data}
        self.on_stop_recording.emit(emit_obj)
        cv2.destroyAllWindows()
        cap.release()

    def process_circles(self, frame, circles):
        """Appends data to the arrays and draws circles in the frame

           DOC: habrá un subarray de 'np.nan' al principio de cada x_data y
           y_data. De esta forma se tendrá sincronizado el momento en el
           que el micro se coloca en posición
        Args:
            frame ([type]): [description]
            circles ([type]): [description]
        """
        if circles is None:

            # if len(self.x_data) != 0:
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
        # TODO: quitar flip en production phase
        frame = cv2.flip(frame, 1)
        self._grid.draw_grid(frame)
        self.process_circles(frame, get_circles(get_mask(frame)))
        self.draw_rec_indicator(frame)

        # TODO: add Time calculation with alpha channel!
        # TODO: fade green to red
        # rgb_times = (self.times*255)/3
        # rgb_times = np.clip(rgb_times, 0, 255).astype(np.uint8)
        # frame = cv2.resize(
        #     rgb_times, (self._grid.size_of_frame[0],
        #                 self._grid.size_of_frame[1]))

        delta = time.time() - self.time
        self.time = time.time()

        if self.x != -1 and self.y != -1:
            grid = self._grid.locate_point((self.x, self.y))
            self.times[grid[1]][grid[0]] += delta
            imb.draw_text(frame, f'{grid[0], grid[1]}', 15, 15)

        return frame

    def draw_rec_indicator(self, frame):
        cv2.circle(
            frame, (self._grid.size_of_frame[0]-30, 30), 8, (0, 0, 255), -1)

    def bypass(self, frame):
        # TODO: quitar flip en prod.
        frame = cv2.flip(frame, 1)
        self._grid.draw_grid(frame)
        return frame

    def rec(self):
        self._rec = True
        print("Start recording!")

    def stop_rec(self):
        self._rec = False
        print("Stop recording!")

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._rec = False
        self._running = False
        self.wait()
