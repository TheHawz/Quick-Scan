# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 12:57:19 2021

@author: pablo
"""

import numpy as np
import cv2
from .imbasic import resize


class Grid:
    """Class that provides the information and methods related to the
    Planar Grid Discretization method.

    Attributes:
        size_of_frame (list): Size of the frame in pixels, in the form
            of first vertical value the the horizontal value.
        number_of_rows (int)
        number_of_cols (int)
        padding (int, optional): Padding arround the borders for the grid.
            Defaults to 0.
        grid_size (np.ndarray): Size of the total grid.
        region_size (np.ndarray): Size of a region of the grid
        hor_div (np.ndarray): List containing the values for horizontal
            divisions in the grid system
        ver_div (np.ndarray): List containing the values for vertical
            divisions in the grid system
    """

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
        self.size_of_frame = np.array([int(i) for i in size_of_frame])
        self.config(number_of_rows, number_of_cols, padding)

    def __repr__(self):
        frame_size = self.size_of_frame
        msg = f'Frame size: [{frame_size[0]},{frame_size[1]}] | '
        msg += f'Rows: {self.number_of_rows} | Cols: {self.number_of_cols}'
        return msg

    def config(self,  number_of_rows, number_of_cols, pad=0):
        """Set ups the whole config for the Grid object

        Each time any of the params changes, there other internal params that
        need to be updated.

        Args:
            number_of_rows (int)
            number_of_cols (int)
            padding (int, optional): Padding arround the borders for the grid.
                Defaults to 0.
        """

        self.number_of_rows = number_of_rows
        self.number_of_cols = number_of_cols
        self.padding = pad
        self.padding_coords = np.array(
            [self.padding, self.padding]).astype(int)

        self.grid_size = np.round(
            self.size_of_frame - (self.padding_coords * 2)).astype(int)

        self.region_size = np.array(
            [self.grid_size[0] / number_of_rows,
             self.grid_size[1] / number_of_cols])

        self.hor_div = [int(self.grid_size[0] / number_of_rows * i + pad)
                        for i in range(number_of_rows + 1)]
        self.ver_div = [int(self.grid_size[1] / number_of_cols * i + pad)
                        for i in range(number_of_cols + 1)]

    def locate_point(self, point: list):
        """ Located a point in the actual grid system.

        Steps:
        1. Invert the point coords to fullfil our notation system (rows, colss)
        2. First substract the padding => to find the coordinate of the point
            in relation to the Origin of the Grid system
        3. Divide by the grid size ([height, width]) and 'floor' the number

        Args:
            point (list): Point in the form of [x, y]. Being x the horizontal
            coordinate and y the vertical coord. It has to be inverted in this
            function in order to satisfy our notation system (rows, columns).

        Returns:
            np.ndarray: Grid the point is at, in the form of a np.ndarray
        """

        point_grid_coords = np.array([point[1], point[0]])
        point_grid_coords -= self.padding_coords

        result = np.floor(point_grid_coords / self.region_size).astype(int)

        # TODO: this can be simplified => using boolean indexes to acces
        # TODO: the array.
        if result[0] >= self.number_of_rows:
            return None
        if result[1] >= self.number_of_cols:
            return None
        if (result < 0).any():
            return None

        return result

    def get_region(self, region):
        """Returns the points that define a region in the grid.

        Args:
            region (tuple[int, int]): [row, col]

        Returns:
            list: [Upper-left corner and lower-right (x, y). OpenCV coords

        Returns None in case that the region was ilegal.
        """

        if region[0] > self.number_of_rows-1 or region[0] < 0:
            return None
        if region[1] > self.number_of_cols-1 or region[1] < 0:
            return None

        reg = np.array(region)

        _pt1 = (self.region_size * reg) + self.padding_coords
        _pt2 = (self.region_size *
                (reg + np.array([1, 1]))) + self.padding_coords

        pt1 = [int(p) for p in [_pt1[1], _pt1[0]]]
        pt2 = [int(p) for p in [_pt2[1], _pt2[0]]]

        return [pt1, pt2]

    def draw_grid(self, frame, color=(180, 180, 180), thickness=1):
        """Draws the grid in a image.

        It ensures that the frame is of the correct size, just in case
        it has been resized.

        Args:
            frame (np.ndarray): Image.
            color (tuple, optional): COlor in rgb. Defaults to (180, 180, 180).
            thickness (int, optional): Thickness of the lines. Defaults to 1.

        Returns:
            np.ndarray: The image with the frame on it.
        """
        w = frame.shape[1]
        _big_frame = resize(frame, width=self.size_of_frame[1])

        for div in self.hor_div:
            start_point = (self.padding, div)
            end_point = (self.size_of_frame[1]-self.padding, div)
            cv2.line(_big_frame, start_point, end_point, color, thickness)

        for div in self.ver_div:
            start_point = (div, self.padding)
            end_point = (div, self.size_of_frame[0]-self.padding)
            cv2.line(_big_frame, start_point, end_point, color, thickness)

        return resize(_big_frame, width=w)
