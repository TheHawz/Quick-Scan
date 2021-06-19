# -*- coding: utf-8 -*-
"""Basic package for image processing.

It is basicaly a OpenCV "wrapper" that allows the users to add functionality
on top of the basic OpenCv functions-
"""

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


def is_image(frame) -> bool:
    """Returns where the object is a image or not.
    """

    return np.shape(frame) != ()


def remove_borders(frame: np.ndarray, amount: int, borders=Borders.ALL):
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

    For efficiency we are extracting the rectangle from the main image,
    creating the color rectangle then use cv2.addWeighted to merge the
    rectangle with the color rectangle, then replacing the pixels in the
    main image with the subimage we've just build.

    Args:
        img (np.ndarray): the image.
        pt1 (list | np.array | tuple): [x1, y1]
        pt2 (list | np.array | tuple): [x2, y2]
        color (list): The color of the rectangle in BGR
        alpha (float): The transparency, between 0 and 1.

    Returns:
        np.ndarray: the image with the rectangle drawn.
    """

    # First we crop the sub-rect from the image
    x1, y1 = pt1
    x2, y2 = pt2
    sub_img = img[y1:y2, x1:x2]

    # Create the colored rectangle.
    white_rect = np.ones(sub_img.shape, dtype=np.uint8) * \
        np.array(color, dtype=np.uint8)

    # Add both subimages with a certain alpha.:
    res = cv2.addWeighted(sub_img, 1-alpha, white_rect,
                          alpha, 0.0, dtype=8)

    # Putting the image back to its position
    img[y1:y2, x1:x2] = res
    return img


def draw_border(img, pt1, pt2, color, thickness=2):
    """Draw the border of a rectangle defined by its upper-left and lower-right
    corners.

    Args:
        img (np.ndarray): the image
        pt1 (list): upper-left corner
        pt2 (list): lower-right corner
        color (list): the color in BGR
        thickness (int, optional): The thickness of the lines. Defaults to 2.

    Returns:
        np.ndarray: the image with the borders.
    """

    x1, y1 = pt1
    x2, y2 = pt2

    # Define the 4 lines of the rectangle.
    lines = [[(x1, y1), (x1, y2)],  # left
             [(x1, y1), (x2, y1)],  # top
             [(x2, y2), (x1, y2)],  # right
             [(x2, y2), (x2, y1)]]  # botom

    for _pt1, _pt2 in lines:
        img = cv2.line(img, _pt1, _pt2, color, thickness=thickness)

    return img
