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

import typing

from aiohttp import payload, web

# pylint: disable=unused-variable


def serialize_response(response: web.Response) -> dict[str, typing.Any]:
    """Serialize an aiohttp response to a dictionary."""
    if (body := response.body) is None:
        body_decoded = None
    elif isinstance(body, payload.StringPayload):
        # pylint: disable=protected-access
        body_decoded = body._value.decode(body.encoding)
    elif isinstance(body, bytes):
        body_decoded = body.decode(response.charset or "utf-8")
    else:
        raise ValueError("Unknown payload encoding")

    return {
        "status": response.status,
        "body": body_decoded,
        "headers": dict(response.headers),
    }
