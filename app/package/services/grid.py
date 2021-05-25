# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 12:57:19 2021

@author: pablo
"""

import numpy as np
import cv2


class Grid:

    def __init__(self,
                 size_of_frame: np.ndarray,
                 number_of_rows: int,
                 number_of_cols: int,
                 padding: int = 0):
        """Constructor

        Args:
            size_of_frame (np.ndarray): (vertical, horizontal). The Grid
            system's convention: [rows, cols] (the same!)
            number_of_rows (int): Vertical
            number_of_cols (int): Horizontal
            padding (int, optional): Padding arround the border. Defaults to 0.
        """
        self.size_of_frame = size_of_frame
        self.config(number_of_rows, number_of_cols, padding)

    def __repr__(self):
        frame_size = self.size_of_frame
        msg = f'Grid obj: <frame_size: [{frame_size[0]},{frame_size[1]}] | '
        msg += f'rows: {self.number_of_rows} | cols: {self.number_of_cols}>'
        return msg

    def config(self,  number_of_rows, number_of_cols, pad=0):
        self.number_of_rows = number_of_rows
        self.number_of_cols = number_of_cols
        self.padding = pad
        self.padding_coords = np.array(
            [self.padding, self.padding]).astype(int)

        self.real_size = np.round(
            self.size_of_frame - (self.padding_coords * 2)).astype(int)

        self.grid_size = np.array(
            [self.real_size[0] / number_of_rows,
             self.real_size[1] / number_of_cols])

        self.hor_div = [int(self.real_size[0] / number_of_rows * i + pad)
                        for i in range(number_of_rows + 1)]
        self.ver_div = [int(self.real_size[1] / number_of_cols * i + pad)
                        for i in range(number_of_cols + 1)]

        # print(f'Hor div: {self.hor_div}')
        # print(f'Ver div: {self.ver_div}')

    def locate_point(self, point: list):
        """ Located a point in the actual grid system.
        - Invert the point coords to fullfil our notation system (rows, colss).
        - First substract the padding => to find the coordinate of the point
        in relation to the Origin of the Grid system
        - Divide by the grid size ([height, width]) and 'floor' the number



        Args:
            point (list): Point in the form of [x, y]. Being x the horizontal
            coordinate and y the vertical coord. It has to be inverted in this
            function in order to satisfy our notation system (rows, columns).

        Returns:
            [np.ndarray]: Grid the point is at, in the form of a np.ndarray
        """
        point_grid_coords = np.array(
            [point[1], point[0]]) - self.padding_coords
        result = np.floor(point_grid_coords / self.grid_size).astype(int)

        # Todo: this can be simplified => using boolean indexes to acces
        # Todo: the array.
        if result[0] >= self.number_of_rows \
                or result[1] >= self.number_of_cols \
                or (result < 0).any():
            return None
        return result

    def get_region(self, region: tuple[int, int]):
        """
        Args:
            region (tuple[int, int]): [row, col]

        Returns:
            pt1: Upper-left corner (x1, y1) Camera's space
            pt1: Lower-right corner  (x2, y2) Camera's space
        """

        # -> self.grid_size  # [vertical, horizontal]

        if (region[0] > self.number_of_rows-1):
            return None
        if (region[1] > self.number_of_cols-1):
            return None

        reg = np.array(region)

        _pt1 = (self.grid_size * reg) + self.padding_coords
        _pt2 = (self.grid_size *
                (reg + np.array([1, 1]))) + self.padding_coords

        pt1 = [int(p) for p in [_pt1[1], _pt1[0]]]
        pt2 = [int(p) for p in [_pt2[1], _pt2[0]]]

        return [pt1, pt2]

    def draw_grid(self, frame, color=(180, 180, 180), thickness=1):
        for div in self.hor_div:
            start_point = (self.padding, div)
            end_point = (self.size_of_frame[1]-self.padding, div)
            cv2.line(frame, start_point, end_point, color, thickness)

        for div in self.ver_div:
            start_point = (div, self.padding)
            end_point = (div, self.size_of_frame[0]-self.padding)
            cv2.line(frame, start_point, end_point, color, thickness)

        return frame

# todo: delete!


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
