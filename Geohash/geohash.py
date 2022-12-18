"""
This file is part of Geohash.

Copyright (C) 2008 Leonard Norrgard <leonard.norrgard@gmail.com>
Copyright (C) 2015 Leonard Norrgard <leonard.norrgard@gmail.com>

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
from math import log10

#  Note: the alphabet in geohash differs from the common base32
#  alphabet described in IETF's RFC 4648
#  (http://tools.ietf.org/html/rfc4648)
_BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"
__decodemap = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "b": 10,
    "c": 11,
    "d": 12,
    "e": 13,
    "f": 14,
    "g": 15,
    "h": 16,
    "j": 17,
    "k": 18,
    "m": 19,
    "n": 20,
    "p": 21,
    "q": 22,
    "r": 23,
    "s": 24,
    "t": 25,
    "u": 26,
    "v": 27,
    "w": 28,
    "x": 29,
    "y": 30,
    "z": 31,
}


def decode_exactly(geohash):
    """
    Decode the geohash to its exact values, including the error
    margins of the result.  Returns four float values: latitude,
    longitude, the plus/minus error for latitude (as a positive
    number) and the plus/minus error for longitude (as a positive
    number).
    """
    lat_interval, lon_interval = (-90.0, 90.0), (-180.0, 180.0)
    lat_err, lon_err = 90.0, 180.0
    is_even = True
    for character in geohash:
        code = __decodemap[character]
        for mask in (16, 8, 4, 2, 1):
            if is_even:  # adds longitude info
                lon_err /= 2
                if code & mask:
                    lon_interval = ((lon_interval[0] + lon_interval[1]) / 2, lon_interval[1])
                else:
                    lon_interval = (lon_interval[0], (lon_interval[0] + lon_interval[1]) / 2)
            else:  # adds latitude info
                lat_err /= 2
                if code & mask:
                    lat_interval = ((lat_interval[0] + lat_interval[1]) / 2, lat_interval[1])
                else:
                    lat_interval = (lat_interval[0], (lat_interval[0] + lat_interval[1]) / 2)
            is_even = not is_even
    lat = (lat_interval[0] + lat_interval[1]) / 2
    lon = (lon_interval[0] + lon_interval[1]) / 2
    return lat, lon, lat_err, lon_err


def decode(geohash):
    """
    Decode geohash, returning two strings with latitude and longitude
    containing only relevant digits and with trailing zeroes removed.
    """
    lat, lon, lat_err, lon_err = decode_exactly(geohash)
    # Format to the number of decimals that are known
    lats = f"{(max(1, int(round(-log10(lat_err)))) - 1, lat)}"
    lons = f"{(max(1, int(round(-log10(lon_err)))) - 1, lon)}"
    if "." in lats:
        lats = lats.rstrip("0")
    if "." in lons:
        lons = lons.rstrip("0")
    return lats, lons


def encode(latitude, longitude, precision: int = 6):
    """
    Encode a position given in float arguments latitude, longitude to
    a geohash which will have the character count precision.
    """
    lat_interval, lon_interval = (-90.0, 90.0), (-180.0, 180.0)
    geohash: list = []
    bits = (16, 8, 4, 2, 1)
    bit = 0
    check = 0
    even = True
    while len(geohash) < precision:
        if even:
            mid = (lon_interval[0] + lon_interval[1]) / 2
            if longitude > mid:
                check |= bits[bit]
                lon_interval = (mid, lon_interval[1])
            else:
                lon_interval = (lon_interval[0], mid)
        else:
            mid = (lat_interval[0] + lat_interval[1]) / 2
            if latitude > mid:
                check |= bits[bit]
                lat_interval = (mid, lat_interval[1])
            else:
                lat_interval = (lat_interval[0], mid)
        even = not even
        if bit < 4:
            bit += 1
        else:
            geohash += _BASE32[check]
            bit = 0
            check = 0
    return "".join(geohash)
