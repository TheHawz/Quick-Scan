# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 13:06:42 2021

@author: pablo
"""

import cv2
from . import colorSegmentation as cs

# TODO: move to own config file
TRACKING_COLOR = (220, 198, 43)  # BGR
BOTTOM_HSV_THRES = (80, 110, 10)
TOP_HSV_THRES = (130, 255, 255)


def improve_mask(mask, morph_type=cv2.MORPH_ELLIPSE, size=(3, 3)):
    kernel = cv2.getStructuringElement(morph_type, size)
    opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return opened


def get_mask(frame):
    mask = cs.getColorMask(frame, BOTTOM_HSV_THRES, TOP_HSV_THRES)
    return improve_mask(mask, cv2.MORPH_ELLIPSE, (7, 7))


def get_circles(mask):
    return cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, dp=3, minDist=150)
