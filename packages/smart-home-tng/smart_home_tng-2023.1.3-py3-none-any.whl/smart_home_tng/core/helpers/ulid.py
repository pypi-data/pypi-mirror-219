"""
Helpers for Components of Smart Home - The Next Generation.

Smart Home - TNG is a Home Automation framework for observing the state
of entities and react to changes. It is based on Home Assistant from
home-assistant.io and the Home Assistant Community.

Copyright (c) 2022-2023, Andreas Nixdorf

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program.  If not, see
http://www.gnu.org/licenses/.
"""

import random
import time

# pylint: disable=unused-variable


def ulid_hex() -> str:
    """Generate a ULID in lowercase hex that will work for a UUID.

    This ulid should not be used for cryptographically secure
    operations.

    This string can be converted with https://github.com/ahawker/ulid

    ulid.from_uuid(uuid.UUID(ulid_hex))
    """
    return f"{int(time.time()*1000):012x}{random.getrandbits(80):020x}"


def ulid(timestamp: float = None) -> str:
    """Generate a ULID.

    This ulid should not be used for cryptographically secure
    operations.

     01AN4Z07BY      79KA1307SR9X4MV3
    |----------|    |----------------|
     Timestamp          Randomness
       48bits             80bits

    This string can be loaded directly with https://github.com/ahawker/ulid

    import homeassistant.util.ulid as ulid_util
    import ulid
    ulid.parse(ulid_util.ulid())
    """
    ulid_bytes = int((timestamp or time.time()) * 1000).to_bytes(
        6, byteorder="big"
    ) + int(random.getrandbits(80)).to_bytes(10, byteorder="big")

    # This is base32 crockford encoding with the loop unrolled for performance
    #
    # This code is adapted from:
    # https://github.com/ahawker/ulid/blob/06289583e9de4286b4d80b4ad000d137816502ca/ulid/base32.py#L102
    #
    enc = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
    return (
        enc[(ulid_bytes[0] & 224) >> 5]
        + enc[ulid_bytes[0] & 31]
        + enc[(ulid_bytes[1] & 248) >> 3]
        + enc[((ulid_bytes[1] & 7) << 2) | ((ulid_bytes[2] & 192) >> 6)]
        + enc[((ulid_bytes[2] & 62) >> 1)]
        + enc[((ulid_bytes[2] & 1) << 4) | ((ulid_bytes[3] & 240) >> 4)]
        + enc[((ulid_bytes[3] & 15) << 1) | ((ulid_bytes[4] & 128) >> 7)]
        + enc[(ulid_bytes[4] & 124) >> 2]
        + enc[((ulid_bytes[4] & 3) << 3) | ((ulid_bytes[5] & 224) >> 5)]
        + enc[ulid_bytes[5] & 31]
        + enc[(ulid_bytes[6] & 248) >> 3]
        + enc[((ulid_bytes[6] & 7) << 2) | ((ulid_bytes[7] & 192) >> 6)]
        + enc[(ulid_bytes[7] & 62) >> 1]
        + enc[((ulid_bytes[7] & 1) << 4) | ((ulid_bytes[8] & 240) >> 4)]
        + enc[((ulid_bytes[8] & 15) << 1) | ((ulid_bytes[9] & 128) >> 7)]
        + enc[(ulid_bytes[9] & 124) >> 2]
        + enc[((ulid_bytes[9] & 3) << 3) | ((ulid_bytes[10] & 224) >> 5)]
        + enc[ulid_bytes[10] & 31]
        + enc[(ulid_bytes[11] & 248) >> 3]
        + enc[((ulid_bytes[11] & 7) << 2) | ((ulid_bytes[12] & 192) >> 6)]
        + enc[(ulid_bytes[12] & 62) >> 1]
        + enc[((ulid_bytes[12] & 1) << 4) | ((ulid_bytes[13] & 240) >> 4)]
        + enc[((ulid_bytes[13] & 15) << 1) | ((ulid_bytes[14] & 128) >> 7)]
        + enc[(ulid_bytes[14] & 124) >> 2]
        + enc[((ulid_bytes[14] & 3) << 3) | ((ulid_bytes[15] & 224) >> 5)]
        + enc[ulid_bytes[15] & 31]
    )
