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

import http
import logging
import typing

import voluptuous as vol
from aiohttp import web

from .smart_home_controller_view import SmartHomeControllerView

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class RequestDataValidator:
    """Validate the incoming data.

    Will return a 400 if no JSON provided or doesn't match schema.
    """

    def __init__(self, schema: vol.Schema, allow_empty: bool = False) -> None:
        """Initialize the decorator."""
        if isinstance(schema, dict):
            schema = vol.Schema(schema)

        self._schema = schema
        self._allow_empty = allow_empty

    async def async_get_request_data(
        self,
        request: web.Request,
    ) -> tuple[typing.Any, web.StreamResponse]:
        """Wrap a request handler with data validation."""
        data = None
        try:
            data = await request.json()
        except ValueError:
            if not self._allow_empty or (await request.content.read()) != b"":
                _LOGGER.error("Invalid JSON received")
                return None, SmartHomeControllerView.json_message(
                    "Invalid JSON.", http.HTTPStatus.BAD_REQUEST
                )
            data = {}

        try:
            data = self._schema(data)
        except vol.Invalid as err:
            _LOGGER.error(f"Data does not match schema: {err}")
            return None, SmartHomeControllerView.json_message(
                f"Message format incorrect: {err}", http.HTTPStatus.BAD_REQUEST
            )
        return data, None
