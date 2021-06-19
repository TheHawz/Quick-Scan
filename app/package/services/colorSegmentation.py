# -*- coding: utf-8 -*-
"""Module for Color Segmentation functions.

Used for segmenting a color object of a frame, and improving the resultant
mask.


Author: Lara Blanco Freire
Modified by: Pablo Losada Rodríguez
"""

import cv2


def getColorMask(img, bottom_thres, top_thres):
    """Returns a mask with the pixels whose values are between the thresholds.

    Args:
        img (np.ndarray, dtype=uint8): Image for processing.
        bottom_thres (list): Threshold in HSV form.
        top_thres (list): Threshold in HSV form.

    Returns:
        np.ndarray: output array of the same size as img and CV_8U type
    """

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, bottom_thres, top_thres)

    return mask
