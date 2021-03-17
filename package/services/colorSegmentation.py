# -*- coding: utf-8 -*-

import cv2
import colorsys

import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import colors


def getColorMask (img, bottom_thres, top_thres):
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


def getColor (img, mask):
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    b_w = cv2.inRange(hsv, (0, 120, 70), (179, 255, 250))
    maskb = cv2.bitwise_and(mask, b_w)
    
    mean = cv2.mean(img, mask=maskb)
    hsv = colorsys.rgb_to_hsv(mean[2] / 179, mean[1] / 255, mean[0] / 255)
    h = hsv[0] * 179
    
    if (h < 10 or h >= 128): return 'o'
    elif (h >= 50 and h < 127): return 'b'
    elif (h >= 10 and h < 40): return 'y'
    else: return None

# MATPLOT LIB DEPENDENCIES
# def showRGBPlot (img):
#     """
    
#     Parameters
#     ----------
#     img : ARRAY OF UINT8
#         CREATES A 3D PLOT OF THE RGB COLOR SPACE.

#     """
    
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     r, g, b = cv2.split(img)
#     fig = plt.figure()
#     axis = fig.add_subplot(1, 1, 1, projection="3d")
    
#     pixel_colors = img.reshape((np.shape(img)[0] * np.shape(img)[1], 3))
#     norm = colors.Normalize(vmin=-1., vmax=1.)
#     norm.autoscale(pixel_colors)
#     pixel_colors = norm(pixel_colors).tolist()
#     axis.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker=".")
#     axis.set_xlabel("Red")
#     axis.set_ylabel("Green")
#     axis.set_zlabel("Blue")
#     plt.show()    
    
# def showHSVPlot (img):
#     """
    
#     Parameters
#     ----------
#     img : ARRAY OF UINT8
#         CREATES A 3D PLOT OF THE HSV COLOR SPACE.

#     """
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
#     h, s, v = cv2.split(hsv)
#     fig = plt.figure()
#     axis = fig.add_subplot(1, 1, 1, projection="3d")
    
#     pixel_colors = img.reshape((np.shape(img)[0] * np.shape(img)[1], 3))
#     norm = colors.Normalize(vmin=-1., vmax=1.)
#     norm.autoscale(pixel_colors)
#     pixel_colors = norm(pixel_colors).tolist()
#     axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
#     axis.set_xlabel("Hue")
#     axis.set_ylabel("Saturation")
#     axis.set_zlabel("Value")
#     plt.show()

