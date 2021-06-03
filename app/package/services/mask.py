# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 13:06:42 2021

@author: pablo
"""

import cv2
from . import colorSegmentation as cs
from .imbasic import resize

# TODO: move to own config file
TRACKING_COLOR = (220, 198, 43)  # BGR
BOTTOM_HSV_THRES = (85, 80, 30)
TOP_HSV_THRES = (125, 255, 225)


def improve_mask(mask, operation, morph_type=cv2.MORPH_ELLIPSE, size=(3, 3)):
    kernel = cv2.getStructuringElement(morph_type, size)
    opened = cv2.morphologyEx(mask, operation, kernel)
    return opened


def get_mask(frame, openSize=3, closeSize=15):
    w = frame.shape[1]
    frame = resize(frame, width=500)
    mask = cs.getColorMask(frame, BOTTOM_HSV_THRES, TOP_HSV_THRES)
    mask = improve_mask(mask, cv2.MORPH_OPEN,
                        cv2.MORPH_ELLIPSE, (openSize, openSize))
    mask = improve_mask(mask, cv2.MORPH_CLOSE,
                        cv2.MORPH_ELLIPSE, (closeSize, closeSize))

    return resize(mask, width=w)


def get_circles(mask, dp=3, minDist=150):
    return cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, dp=dp, minDist=minDist)
