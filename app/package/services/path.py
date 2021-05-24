# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 18:16:28 2021

@author: pablo
"""

import numpy as np

__all__ = ['interpolate_coords']


def interpolate_coords(array: np.ndarray) -> tuple:
    """Trims the array of possible np.nan values at the end of the
    array and interpolates any np.nan value that is located in the array

    Args:
        array (np.array): Initial array

    Returns:
        np.array: processed array
    """

    array = _typesignal(array)

    # 1. Trim
    array, shift = _trim_first_nans(array)
    array, trim = _trim_last_nans(array)

    # 2. Interpolate
    x_nans, x_nonzero = _nan_helper(array)
    array[x_nans] = np.interp(
        x_nonzero(x_nans), x_nonzero(~x_nans), array[~x_nans])
    return array, shift, trim


def _typesignal(value):
    if type(value) is list:
        return np.array(value)
    if type(value) is np.ndarray:
        return value
    raise Exception(
        f'Data.x and Data.y are in a non supported format: {type(value)}')


def _nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    """

    return np.isnan(y), lambda z: z.nonzero()[0]


def _trim_first_nans(array):

    i = 0
    le = len(array)
    while i < le:
        if not np.isnan(array[i]):
            break
        i += 1

    array = array[i:]

    return array, i


def _trim_last_nans(array, verbose=False):
    """Search for a block of np.nan at the end of the array
    and returns the same array without the np.nan at the end.

    Args:
        array (np.array): initial array
        verbose (bool, optional): Whether the funcion should
        print extra information or not. Use only for debugin
        purpose. Defaults to False.

    Returns:
        np.array: trimed array
    """

    array_rev = array[::-1]
    i = 0
    le = len(array_rev)
    while i < le:
        i += 1
        if not np.isnan(array_rev[i]):
            break

    array_rev = array_rev[i:]

    return array_rev[::-1], i
