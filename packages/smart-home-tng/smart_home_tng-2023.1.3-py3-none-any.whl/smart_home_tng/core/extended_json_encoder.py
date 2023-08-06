"""
Core components of Smart Home - The Next Generation.

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

import datetime
import typing

from .json_encoder import JsonEncoder


# pylint: disable=unused-variable
class ExtendedJsonEncoder(JsonEncoder):
    """JSONEncoder that supports Home Assistant objects and falls back to repr(o)."""

    def default(self, o: typing.Any) -> typing.Any:
        """Convert certain objects.

        Fall back to repr(o).
        """
        if isinstance(o, datetime.timedelta):
            return {"__type": str(type(o)), "total_seconds": o.total_seconds()}
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, (datetime.date, datetime.time)):
            return {"__type": str(type(o)), "isoformat": o.isoformat()}
        try:
            return super().default(o)
        except TypeError:
            return {"__type": str(type(o)), "repr": repr(o)}
