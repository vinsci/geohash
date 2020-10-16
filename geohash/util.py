from typing import Tuple

import numpy as np

#  Note: the alphabet in geohash differs from the common base32
#  alphabet described in IETF's RFC 4648
#  (http://tools.ietf.org/html/rfc4648)
__base32 = "0123456789bcdefghjkmnpqrstuvwxyz"
base32 = np.array(list(__base32))
bit_mask = np.array([16, 8, 4, 2, 1])

decodemap = {}
for i in range(len(__base32)):
    decodemap[__base32[i]] = i
del i


def get_intervals(n_points: int) -> Tuple[np.array, np.array]:
    """
    Get vectors (np.arrays) of the latitude and longitude intervals (limits)

    Args:
        ``n_points`` (`int`): Shape of arrays needed.

    Returns:
        `tuple` of numpy arrays; the shape of each array is (2, `n_points`) with
        the first index corresponding to latitude limits.
    """
    ones = np.ones(n_points)
    lat_interval = np.array([ones * -90.0, ones * 90.0])
    lon_interval = np.array([ones * -180.0, ones * 180.0])
    return (lat_interval, lon_interval)


def get_precision(error: np.array) -> int:
    precision = np.around(-np.log10(error)).astype(int) - 1
    pmax = np.max(precision)
    return max(1, pmax)
