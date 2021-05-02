# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 12:57:19 2021

@author: pablo
"""

import numpy as np
import cv2


class Grid:

    def __init__(self, size_of_frame, number_of_rows, number_of_cols, padding=0):
        """Constructor

        Args:
            size_of_frame (numpy.array): (horizontal, vertical)
            number_of_rows (int): 
            number_of_cols (int): 
            padding (int, optional): Padding arround the border. Defaults to 0.
        """
        self.size_of_frame = size_of_frame
        self.config(number_of_rows, number_of_cols, padding)

    def config(self,  number_of_rows, number_of_cols, padding=0):
        self.number_of_rows = number_of_rows
        self.number_of_cols = number_of_cols
        self.padding = padding
        self.padding_coords = np.array(
            [self.padding, self.padding]).astype(int)

        self.real_size = np.round(
            self.size_of_frame - (self.padding_coords * 2)).astype(int)

        self.grid_size = np.array(
            [self.real_size[0] / self.number_of_rows,
             self.real_size[1] / self.number_of_cols])

        self.hor_div = [int(self.real_size[1] / self.number_of_rows * i + padding)
                        for i in range(self.number_of_rows + 1)]
        self.ver_div = [int(self.real_size[0] / self.number_of_cols * i + padding)
                        for i in range(self.number_of_cols + 1)]

    def locate_point(self, point):
        point_grid_coords = np.array(point) - self.padding_coords
        return np.floor(point_grid_coords / self.grid_size).astype(int)

    def draw_grid(self, frame, color=(180, 180, 180), thickness=1):
        for div in self.hor_div:
            start_point = (self.padding, div)
            end_point = (self.size_of_frame[0]-self.padding, div)
            cv2.line(frame, start_point, end_point, color, thickness)

        for div in self.ver_div:
            start_point = (div, self.padding)
            end_point = (div, self.size_of_frame[1]-self.padding)
            cv2.line(frame, start_point, end_point, color, thickness)

        return frame


def draw_grid(frame, rows, cols, padding, color=(180, 180, 180), thickness=1):
    """ 
        TODO: se puede optimizar mucho: 
        crear una mascara que luego se reutilice para colorear todos 
        los frames siguientes
    """
    # GET SIZE OF THE FRAME & APPLY PADDING
    x_size, y_size = frame.shape[:2]

    real_x_size = x_size - (padding * 2)
    real_y_size = y_size - (padding * 2)

    hor_div = [int(real_x_size / rows * i + padding) for i in range(rows + 1)]
    ver_div = [int(real_y_size / cols * i + padding) for i in range(cols + 1)]

    # DRAW HORIZONTAL DIVISIONS
    for div in hor_div:
        start_point = (padding, div)
        end_point = (y_size - padding, div)
        cv2.line(frame, start_point, end_point, color, thickness)

    # DRAW VERTICAL DIVISIONS
    for div in ver_div:
        start_point = (div, padding)
        end_point = (div, x_size - padding)
        cv2.line(frame, start_point, end_point, color, thickness)

    return frame
