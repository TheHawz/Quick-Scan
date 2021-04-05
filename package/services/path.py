# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 18:16:28 2021

@author: pablo
"""

import numpy as np


def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    """

    return np.isnan(y), lambda z: z.nonzero()[0]


def trim_last_nans(array, verbose=False):
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

    if verbose:
        print(f'Initial length of array: {len(array)}')

    array_rev = array[::-1]
    i = 0
    while True:
        i += 1
        if not np.isnan(array_rev[i]):
            break

    if verbose:
        print(f'Triming last block of Nan values: length = {i}')

    array_rev = array_rev[i:]

    if verbose:
        print(f'Actual length of the Array: {len(array_rev)}')

    if len(array_rev) != len(array)-i:
        print('[ERROR] Trim procedure failed!')
        return Exception

    return array_rev[::-1]


def interpolate_nan(array):
    """Trims the array of possible np.nan values at the end of the 
    array and interpolates any np.nan value that is located in the array

    Args:
        array (np.array): Initial array

    Returns:
        np.array: processed array
    """
    array = np.array(trim_last_nans(array, True))
    x_nans, x_nonzero = nan_helper(array)
    array[x_nans] = np.interp(
        x_nonzero(x_nans), x_nonzero(~x_nans), array[~x_nans])
    return array
