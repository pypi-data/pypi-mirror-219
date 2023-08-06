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
from .request_data_validator import RequestDataValidator
from .unknown_flow import UnknownFlow

_VALIDATOR: typing.Final = RequestDataValidator(vol.Schema(dict), allow_empty=True)


# pylint: disable=unused-variable
class FlowManagerResourceView(_BaseFlowManagerView):
    """View to interact with the flow manager."""

    async def get(self, _request: web.Request, flow_id: str) -> web.Response:
        """Get the current state of a data_entry_flow."""
        try:
            result = await self._flow_mgr.async_configure(flow_id)
        except UnknownFlow:
            return self.json_message(
                "Invalid flow specified", http.HTTPStatus.NOT_FOUND
            )

        result = self._prepare_result_json(result)

        return self.json(result)

    async def post(self, request: web.Request, flow_id: str) -> web.Response:
        """Handle a POST request."""
        data, error = await _VALIDATOR.async_get_request_data(request)
        if error is not None:
            return error

        try:
            result = await self._flow_mgr.async_configure(flow_id, data)
        except UnknownFlow:
            return self.json_message(
                "Invalid flow specified", http.HTTPStatus.NOT_FOUND
            )
        except vol.Invalid as ex:
            return self.json_message(
                f"User input malformed: {ex}", http.HTTPStatus.BAD_REQUEST
            )

        result = self._prepare_result_json(result)

        return self.json(result)

    async def delete(self, _request: web.Request, flow_id: str) -> web.Response:
        """Cancel a flow in progress."""
        try:
            self._flow_mgr.async_abort(flow_id)
        except UnknownFlow:
            return self.json_message(
                "Invalid flow specified", http.HTTPStatus.NOT_FOUND
            )

        return self.json_message("Flow aborted")
