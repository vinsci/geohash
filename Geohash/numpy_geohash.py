"""
Copyright (C) 2008 Leonard Norrgard <leonard.norrgard@gmail.com>
Copyright (C) 2015 Leonard Norrgard <leonard.norrgard@gmail.com>

This file is part of Geohash.

Geohash is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Geohash is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public
License along with Geohash.  If not, see
<http://www.gnu.org/licenses/>.
"""

import numpy as np

#  Note: the alphabet in geohash differs from the common base32
#  alphabet described in IETF's RFC 4648
#  (http://tools.ietf.org/html/rfc4648)
__base32 = np.array(list('0123456789bcdefghjkmnpqrstuvwxyz'))


def numpy_encode(latitude: np.array, longitude: np.array, precision: int =12) -> np.array:
    """
    Geohash vectors of latitiude and longitude to a given precision.
    
    Parameters
    ----------
    latitude: np.array
    longitude: np.array
    precision: int
    
    Returns
    -------
    geohash: np.array
    """
    n_points = len(latitude)
    assert(len(latitude) == len(longitude))
    ones = np.ones(n_points)
    lat_interval = np.array([ones * -90.0, ones * 90.0])
    lon_interval = np.array([ones * -180.0, ones * 180.0])
    geohash = []
    bits = [ 16, 8, 4, 2, 1 ]
    bit = 0
    ch = np.zeros(n_points, dtype=int)
    even = True

    while len(geohash) < precision:
        if even:
            mid = (lon_interval[0] + lon_interval[1]) / 2
            msk = longitude > mid
            ch_bits = bits[bit]
            ch[msk] = np.bitwise_or(ch[msk], ch_bits)
            lon_interval[0, msk] = mid[msk]
            lon_interval[1, np.invert(msk)] = mid[np.invert(msk)]
        else:
            mid = (lat_interval[0] + lat_interval[1]) / 2
            msk = latitude > mid
            ch_bits = bits[bit]
            ch[msk] = np.bitwise_or(ch[msk], ch_bits)
            lat_interval[0, msk] = mid[msk]
            lat_interval[1, np.invert(msk)] = mid[np.invert(msk)]

        even = not even
        if bit < 4:
            bit += 1
        else:
            geohash.append(__base32[ch])
            bit = 0
            ch = np.zeros(n_points, dtype=int)

    return np.array(list(map(''.join, zip(*geohash))))
