# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 13:06:42 2021

@author: pablo
"""

import cv2

def improve_mask(mask, morph_type = cv2.MORPH_ELLIPSE, size = (3, 3)):
    kernel = cv2.getStructuringElement(morph_type, size)
    opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return opened