from typing import Tuple, Union

import numpy as np

import geohash as gh


def encoder(
    latitude: Union[np.array, float], longitude: Union[np.array, float], precision: int = 12
) -> Union[np.array, str]:
    """
    Encode a position given in float arguments latitude, longitude to
    a geohash which will have the character count precision.

    Args:
        ``latitude`` (`float` or `np.array`)
        ``longitude`` (`float` or `np.array`)
        ``precision`` (`int`)

    Returns:
        ``geohash`` (`str` or `np.array`)
    """
    if isinstance(latitude, np.ndarray) and isinstance(longitude, np.ndarray):
        return array(latitude, longitude, precision)

    return point(latitude, longitude, precision=precision)


def array(latitude: np.array, longitude: np.array, precision: int = 12) -> np.array:
    """
    Geohash vectors of latitiude and longitude to a given precision.

    Args:
        ``latitude`` (`np.array`): Array of latitude
        ``longitude`` (`np.array`): Array of longitudes
        ``precision`` (`int`): How precise you'd like

    Returns:
        ``geohash`` (`np.array`): Array of geo hashes
    """
    n_points = len(latitude)
    if not (latitude.shape == longitude.shape):
        raise ValueError(f"Arrays are not the same shapes {latitude.shape}, {longitude.shape}")

    lat_interval, lon_interval = gh.util.get_intervals(n_points)
    geohash = []
    bit = 0
    ch = np.zeros(n_points, dtype=int)
    even = True

    while len(geohash) < precision:
        if even:
            mid = (lon_interval[0] + lon_interval[1]) / 2
            msk = longitude > mid
            ch_bits = gh.util.bit_mask[bit]
            ch[msk] = np.bitwise_or(ch[msk], ch_bits)
            lon_interval[0, msk] = mid[msk]
            lon_interval[1, np.invert(msk)] = mid[np.invert(msk)]
        else:
            mid = (lat_interval[0] + lat_interval[1]) / 2
            msk = latitude > mid
            ch_bits = gh.util.bit_mask[bit]
            ch[msk] = np.bitwise_or(ch[msk], ch_bits)
            lat_interval[0, msk] = mid[msk]
            lat_interval[1, np.invert(msk)] = mid[np.invert(msk)]

        even = not even
        if bit < 4:
            bit += 1
        else:
            geohash.append(gh.util.base32[ch])
            bit = 0
            ch = np.zeros(n_points, dtype=int)

    return np.array(list(map("".join, zip(*geohash))))


def point(latitude: float, longitude: float, precision: int = 12) -> str:
    """
    Encode a position given in float arguments latitude, longitude to
    a geohash which will have the character count precision.

    Args:
        ``latitude`` (`float`)
        ``longitude`` (`float`)
        ``precision`` (`int`)

    Returns:
        ``geohash`` (`str`)
    """
    return array(np.array([latitude]), np.array([longitude]), precision=precision)[0]
