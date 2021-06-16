# -*- coding: utf-8 -*-

from enum import Enum
import numpy as np
import cv2


class Borders(Enum):
    ALL = 0
    VERTICAL = 1
    HORIZONTAL = 2


def to_tuple(a):
    try:
        return tuple(to_tuple(i) for i in a)
    except TypeError:
        return a


def is_image(frame):
    return np.shape(frame) != ()


def remove_borders(frame, amount, borders=Borders.ALL):
    if not is_image(frame):
        raise Exception("Param. FRAME is not an image.")

    if amount == 0:
        return frame

    h, w = frame.shape[:2]
    r = int(amount / 2)

    if borders == Borders.ALL:
        return frame[r:h-r, r:w-r]
    elif borders == Borders.HORIZONTAL:
        return frame[:, r:w-r]
    elif borders == Borders.VERTICAL:
        return frame[r:h-r, :]
    else:
        raise Exception("Param. BORDERS does not have the correct format.")


def imshow(frame, win_name="img", size=None, width=None):

    if not is_image(frame):
        return

    resized_frame = resize(frame, size=size, width=width)
    cv2.imshow(win_name, resized_frame)


def resize(frame, size=None, width=None, return_scale_factor=False):
    if width is None:
        scale_factor = 1
    else:
        w = frame.shape[1]
        scale_factor = width/w

    frame = cv2.resize(frame, size, fx=scale_factor, fy=scale_factor)

    if return_scale_factor:
        return frame, scale_factor

    return frame


def draw_text(img, text, x, y, color=(255, 255, 255)):
    return cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, color, 1)


def draw_filled_rectangle(img, pt1, pt2, color, alpha):
    """Draw a color rectangle in img from pt1 to pt2 of color "Gray" with
    alpha of "alpha"

    Args:
        img ([type]): [description]
        pt1 (list | np.array | tuple): [x1, y1]
        pt2 (list | np.array | tuple): [x2, y2]
        gray ([type]): [description]
        alpha ([type]): [description]

    Returns:
        [type]: [description]
    """
    # First we crop the sub-rect from the image
    x1, y1 = pt1
    x2, y2 = pt2

    sub_img = img[y1:y2, x1:x2]
    white_rect = np.ones(sub_img.shape, dtype=np.uint8) * \
        np.array(color, dtype=np.uint8)

    # Added with the form:
    res = cv2.addWeighted(sub_img, 1-alpha, white_rect,
                          alpha, 0.0, dtype=8)

    # Putting the image back to its position
    img[y1:y2, x1:x2] = res
    return img


def draw_border(img, pt1, pt2, color, thickness=2):
    x1, y1 = pt1
    x2, y2 = pt2

    lines = [[(x1, y1), (x1, y2)],
             [(x1, y1), (x2, y1)],
             [(x2, y2), (x1, y2)],
             [(x2, y2), (x2, y1)]]

    for _pt1, _pt2 in lines:
        img = cv2.line(img, _pt1, _pt2, color, thickness=thickness)

    return img
