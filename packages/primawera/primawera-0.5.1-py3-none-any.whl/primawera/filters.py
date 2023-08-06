"""
Implementation of various filters that Primawera uses.
"""
import numpy as np
from numpy.typing import ArrayLike


# Expects an array with dtype=float
def linear_stretch(array: ArrayLike) -> ArrayLike:
    """
    Linearly stretches the data inside the array to range [0.0, 1.0].

    Parameters
    ----------
    array: ndarray of type float.
        Data to strech.

    Returns
    -------
    out: ndarray of type float
        New array filled with stretched data.

    """
    array = np.array(array, dtype=float, copy=True)
    frames, height, width = array.shape
    max_val, min_val = np.max(array), np.min(array)
    if max_val - min_val == 0:
        print("Error: Cannot apply linear stretch filter on constant images, "
              "which would cause a division by 0 error! Ignoring filter.")
        return array
    factor = 1.0 / (max_val - min_val)
    for n in range(frames):
        array[n] = array[n] - min_val
        array[n] = array[n] * factor
    return array


def gamma_correction(array: ArrayLike, factor: float) -> ArrayLike:
    """
    Applies gamma correction with the given factor.

    Parameters
    ----------
    array: ndarray
        Input data.
    factor: float
        Gamma correction factor.

    Returns
    -------
    array: ndarray float
        New array with gamma correction applied.
    """
    array = np.array(array, dtype=float, copy=True)
    max_value = array.max()
    array = array / max_value
    array **= factor
    array *= max_value
    return array


def linear_contrast(array: ArrayLike, factor: float) -> ArrayLike:
    modified = array * factor
    return modified


def logarithm_stretch(array: ArrayLike, factor=1.0) -> ArrayLike:
    """
    Apply logarithm stretch to the data.

    Result is calculated as taking the natural logarithm of the data and then
    multiplied by the passed in factor.

    If the data contains negatives values, the transformation is applied on
    the absolute value of the data, and then the signs are reapplied.

    Parameters
    ----------
    array: ArrayLike
        Input data.
    factor: float
        Multiplication factor.

    Returns
    -------
    result: ArrayLike
        Stretched data.

    """
    array = np.asanyarray(array)
    shift = False
    original_signs = None
    if array.min() < 0:
        shift = True
        original_signs = np.sign(array)
        array = np.abs(array)
    result = factor * np.log(array + 1)
    if shift:
        result = result * original_signs
    return result
