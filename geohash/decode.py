from typing import Tuple, Union
import copy

import numpy as np

import geohash as gh


def decoder(geohash: Union[np.array, str]) -> Union[np.array, str]:
    """
    Decode a position given in float arguments latitude, longitude to
    a geohash which will have the character count precision.

    Args:
        ``geohash`` (`float` or `np.array`)

    Returns:
        `tuple of `np.array`: `latitude`, `longitude`, plus/minus `error` for `latitude` and `longitude`
    """
    if isinstance(geohash, np.ndarray):
        return array(geohash)

    return point(geohash)


def _apply_mask(hash_int: np.array, interval: np.array, error: np.array, bit: int) -> Tuple[np.array, np.array]:
    """
    Apply the mask and update each entry accordingly.
    """
    interval = copy.deepcopy(interval)
    error = copy.deepcopy(error)

    error /= 2
    msk = np.bitwise_and(hash_int, bit) != 0
    imsk = np.invert(msk)

    mid = (interval[0] + interval[1]) / 2
    interval[0, msk] = mid[msk]
    interval[1, imsk] = mid[imsk]

    return interval, error


def _decoder(arr: np.array) -> np.array:
    """
    Decode the numpy array from str to int, via masking
    rather than straight lookup.
    """
    decoded = np.zeros(arr.shape)
    for k, v in gh.util.decodemap.items():
        decoded[arr == k] = v
    return decoded


def exact(geohash: np.array) -> Tuple[np.array, np.array, np.array, np.array]:
    """
    Decode the geohash to its exact values, including the error
    margins of the result.

    Only goes to precision of first entry in array.

    Args:
        ``geohash`` (`str`)

    Returns:
        `tuple of `np.array`: `latitude`, `longitude`, plus/minus `error` for `latitude` and `longitude`
    """
    n_points = len(geohash)
    lat_interval, lon_interval = gh.util.get_intervals(n_points)
    lat_error, lon_error = np.ones(n_points) * 90.0, np.ones(n_points) * 180.0
    precision = len(geohash[0])
    is_even = True

    for i in range(precision):
        h = geohash.view("<U1").reshape(geohash.shape + (-1,))[:, i]
        h = _decoder(h).astype(int)
        for bit in gh.util.bit_mask:
            if is_even:
                lon_interval, lon_error = _apply_mask(h, lon_interval, lon_error, bit)
            else:
                lat_interval, lat_error = _apply_mask(h, lat_interval, lat_error, bit)
            is_even = not is_even
    lat = np.mean(lat_interval, axis=0)
    lon = np.mean(lon_interval, axis=0)
    return lat, lon, lat_error, lon_error


def array(geohash: str) -> Tuple[float, float]:
    """
    Decode geohash, returning two strings with latitude and longitude
    containing only relevant digits and with trailing zeroes removed.

    Args:
        ``geohash`` (`str`)

    Returns:
        `np.array` of `str` to preserve precision
        (`latitude`, `longitude`)
    """
    lat, lon, lat_err, lon_err = exact(geohash)
    p_lat = gh.util.get_precision(lat_err)
    p_lon = gh.util.get_precision(lon_err)
    lat = np.around(lat, p_lat).astype(str)
    lon = np.around(lon, p_lon).astype(str)
    return lat, lon


def point(geohash: str) -> Tuple[float, float]:
    """
    Decode geohash, returning two strings with latitude and longitude
    containing only relevant digits and with trailing zeroes removed.

    Args:
        ``geohash`` (`str`)

    Returns:
        `str`: `latitude`, `longitude`
    """
    lat, lon = array(np.array(geohash))
    lat, lon = lat[0], lon[1]
    return lat[0], lon[0]
