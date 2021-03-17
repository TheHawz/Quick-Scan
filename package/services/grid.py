# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 12:57:19 2021

@author: pablo
"""

import numpy as np
import cv2


class Grid:

    def __init__(self, size_of_frame, number_of_rows, number_of_cols, padding=0):
        self.size_of_frame = size_of_frame
        self.number_of_rows = number_of_rows
        self.number_of_cols = number_of_cols
        self.padding = padding
        
    def locate_point(self, point):
        x_size, y_size = self.size_of_frame
        real_x_size = x_size - (self.padding * 2)
        real_y_size = y_size - (self.padding * 2)
        
        grid_size_x = real_x_size / self.number_of_rows
        grid_size_y = real_y_size / self.number_of_cols
        
        point_grid_coords = np.array(point) - np.array([self.padding, self.padding])
        
        return np.ceil(point_grid_coords / np.array([grid_size_y, grid_size_x]))
        

def draw_grid(frame,
              number_of_rows,
              number_of_cols,
              padding,
              color=(180, 180, 180),
              thickness=1,):
    
    # GET SIZE OF THE FRAME & APPLY PADDING
    x_size, y_size = frame.shape[:2]
    
    real_x_size = x_size - (padding * 2)
    real_y_size = y_size - (padding * 2)
    
    hor_div = [int(real_x_size / number_of_rows * i + padding) for i in range(number_of_rows + 1)]
    ver_div = [int(real_y_size / number_of_cols * i + padding) for i in range(number_of_cols + 1)]

    # DRAW HORIZONTAL DIVISIONS
    for div in hor_div:
        start_point = (padding, div)
        end_point = (y_size - padding, div)
        cv2.line(frame, start_point, end_point, color, thickness) 
    
    # # DRAW VERTICAL DIVISIONS
    for div in ver_div:
        start_point = (div, padding)
        end_point = (div, x_size - padding)
        cv2.line(frame, start_point, end_point, color, thickness) 
        
    return frame
