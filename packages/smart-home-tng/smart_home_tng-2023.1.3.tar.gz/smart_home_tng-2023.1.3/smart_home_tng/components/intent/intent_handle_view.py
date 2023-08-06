"""
Intent Component for Smart Home - The Next Generation.

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

import voluptuous as vol
from aiohttp import web

from ... import core

_cv: typing.TypeAlias = core.ConfigValidation
_const: typing.TypeAlias = core.Const
_intent: typing.TypeAlias = core.Intent

_VALIDATOR: typing.Final = core.RequestDataValidator(
    vol.Schema(
        {
            vol.Required("name"): _cv.string,
            vol.Optional("data"): vol.Schema({_cv.string: object}),
        }
    )
)


# pylint: disable=unused-variable
class IntentHandleView(core.SmartHomeControllerView):
    """View to handle intents from JSON."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        extra_urls: list[str] = None,
        requires_auth=True,
        cors_allowed=False,
    ):
        url = "/api/intent/handle"
        name = "api:intent:handle"
        super().__init__(url, name, extra_urls, requires_auth, cors_allowed)
        self._owner = owner

    async def post(self, request: web.Request):
        """Handle intent with name/data."""
        controller: core.SmartHomeController = request.app[_const.KEY_SHC]
        data, error = await _VALIDATOR.async_get_request_data(request)
        if error is not None:
            return error

        try:
            intent_name = data["name"]
            slots = {
                key: {"value": value} for key, value in data.get("data", {}).items()
            }
            intent_result = await controller.intents.async_handle_intent(
                self._owner.domain, intent_name, slots, "", self.context(request)
            )
        except _intent.IntentHandleError as err:
            intent_result = _intent.Response()
            intent_result.async_set_speech(str(err))

        if intent_result is None:
            intent_result = _intent.Response()
            intent_result.async_set_speech("Sorry, I couldn't handle that")

        return self.json(intent_result)
