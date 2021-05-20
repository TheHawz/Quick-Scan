# -*- coding: utf-8 -*-

import cv2
import colorsys


def getColorMask(img, bottom_thres, top_thres):
    """
    Parameters
    ----------
    img : ARRAY OF UINT8
        THE FUNCTION APPLIES TWO THRESHOLDS.

    Returns
    -------
    mask : ARRAY OF UINT8
        MASK OF PIXELS WITH HIGH SATURATION.

    """

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, bottom_thres, top_thres)
    return mask


def getColor(img, mask):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    b_w = cv2.inRange(hsv, (0, 120, 70), (179, 255, 250))
    maskb = cv2.bitwise_and(mask, b_w)

    mean = cv2.mean(img, mask=maskb)
    hsv = colorsys.rgb_to_hsv(mean[2] / 179, mean[1] / 255, mean[0] / 255)
    h = hsv[0] * 179

    if (h < 10 or h >= 128):
        return 'o'
    elif (h >= 50 and h < 127):
        return 'b'
    elif (h >= 10 and h < 40):
        return 'y'
    else:
        return None
