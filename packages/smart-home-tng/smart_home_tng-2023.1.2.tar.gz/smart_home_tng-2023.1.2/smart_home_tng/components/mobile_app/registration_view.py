"""
Mobile App Component for Smart Home - The Next Generation.

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
import secrets
import typing

import voluptuous as vol
from aiohttp import web
from nacl import secret

from ... import core
from .const import Const
from .helpers import _supports_encryption

_cv: typing.TypeAlias = core.ConfigValidation

_REGISTRATION_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional(Const.ATTR_APP_DATA, default={}): Const.SCHEMA_APP_DATA,
        vol.Required(Const.ATTR_APP_ID): _cv.string,
        vol.Required(Const.ATTR_APP_NAME): _cv.string,
        vol.Required(Const.ATTR_APP_VERSION): _cv.string,
        vol.Required(Const.ATTR_DEVICE_NAME): _cv.string,
        vol.Required(Const.ATTR_MANUFACTURER): _cv.string,
        vol.Required(Const.ATTR_MODEL): _cv.string,
        vol.Optional(core.Const.ATTR_DEVICE_ID): _cv.string,  # Added in 0.104
        vol.Required(Const.ATTR_OS_NAME): _cv.string,
        vol.Optional(Const.ATTR_OS_VERSION): _cv.string,
        vol.Required(Const.ATTR_SUPPORTS_ENCRYPTION, default=False): _cv.boolean,
    },
    # To allow future apps to send more data
    extra=vol.REMOVE_EXTRA,
)

_VALIDATOR: typing.Final = core.RequestDataValidator(_REGISTRATION_SCHEMA)


# pylint: disable=unused-variable
class RegistrationsView(core.SmartHomeControllerView):
    """A view that accepts registration requests."""

    def __init__(self, domain: str):
        url = "/api/mobile_app/registrations"
        name = "api:mobile_app:register"
        super().__init__(url, name)
        self._domain = domain

    async def post(self, request: web.Request) -> web.Response:
        """Handle the POST request for registration."""
        data, error = await _VALIDATOR.async_get_request_data(request)
        if error is not None:
            return error

        shc: core.SmartHomeController = request.app[core.Const.KEY_SHC]

        webhook_id = secrets.token_hex()

        data[core.Const.CONF_WEBHOOK_ID] = webhook_id

        if data[Const.ATTR_SUPPORTS_ENCRYPTION] and _supports_encryption():
            data[Const.CONF_SECRET] = secrets.token_hex(secret.SecretBox.KEY_SIZE)

        data[Const.CONF_USER_ID] = request[core.Const.KEY_SHC_USER].id

        # Fallback to DEVICE_ID if slug is empty.
        if not core.helpers.slugify(data[Const.ATTR_DEVICE_NAME], separator=""):
            data[Const.ATTR_DEVICE_NAME] = data[core.Const.ATTR_DEVICE_ID]

        await shc.async_create_task(
            shc.config_entries.flow.async_init(
                self._domain, data=data, context={"source": "registration"}
            )
        )

        remote_ui_url = None

        return self.json(
            {
                Const.CONF_CLOUDHOOK_URL: None,
                Const.CONF_REMOTE_UI_URL: remote_ui_url,
                Const.CONF_SECRET: data.get(Const.CONF_SECRET),
                core.Const.CONF_WEBHOOK_ID: data[core.Const.CONF_WEBHOOK_ID],
            },
            status_code=http.HTTPStatus.CREATED,
        )
