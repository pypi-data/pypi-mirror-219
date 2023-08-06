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
import typing

import voluptuous as vol
from aiohttp import web

from .base_flow_manager_view import _BaseFlowManagerView
from .config_entry_source import ConfigEntrySource
from .config_validation import ConfigValidation as cv
from .request_data_validator import RequestDataValidator
from .unknown_handler import UnknownHandler
from .unknown_step import UnknownStep

_VALIDATOR: typing.Final[RequestDataValidator] = RequestDataValidator(
    vol.Schema(
        {
            vol.Required("handler"): vol.Any(str, list),
            vol.Optional("show_advanced_options", default=False): cv.boolean,
        },
        extra=vol.ALLOW_EXTRA,
    )
)


# pylint: disable=unused-variable
class FlowManagerIndexView(_BaseFlowManagerView):
    """View to create config flows."""

    async def post(self, request: web.Request) -> web.Response:
        """Handle a POST request."""
        data, error = await _VALIDATOR.async_get_request_data(request)
        if error is not None:
            return error

        if isinstance(data["handler"], list):
            handler = tuple(data["handler"])
        else:
            handler = data["handler"]

        try:
            result = await self._flow_mgr.async_init(
                handler,
                context={
                    "source": ConfigEntrySource.USER,
                    "show_advanced_options": data["show_advanced_options"],
                },
            )
        except UnknownHandler:
            return self.json_message(
                "Invalid handler specified", http.HTTPStatus.NOT_FOUND
            )
        except UnknownStep:
            return self.json_message(
                "Handler does not support user", http.HTTPStatus.BAD_REQUEST
            )

        result = self._prepare_result_json(result)

        return self.json(result)
