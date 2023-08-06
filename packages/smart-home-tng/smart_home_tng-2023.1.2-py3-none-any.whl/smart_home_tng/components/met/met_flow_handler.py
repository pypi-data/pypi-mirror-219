"""
Met Integration for Smart Home - The Next Generation.

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

from ... import core
from .const import Const

_cv: typing.TypeAlias = core.ConfigValidation


# pylint: disable=unused-variable
class MetFlowHandler(core.ConfigFlow):
    """Config flow for Met component."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        context: dict[str, typing.Any] = None,
        data: typing.Any = None,
    ):
        """Init MetFlowHandler."""
        version = 1
        super().__init__(
            owner.controller, owner.domain, context=context, data=data, version=version
        )
        self._errors = {}
        self._owner = owner

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            if (
                f"{user_input.get(core.Const.CONF_LATITUDE)}-"
                + f"{user_input.get(core.Const.CONF_LONGITUDE)}"
                not in _configured_instances(self._owner)
            ):
                return self.async_create_entry(
                    title=user_input[core.Const.CONF_NAME], data=user_input
                )
            self._errors[core.Const.CONF_NAME] = "already_configured"

        return await self._show_config_form(
            name=Const.HOME_LOCATION_NAME,
            latitude=self._shc.config.latitude,
            longitude=self._shc.config.longitude,
            elevation=self._shc.config.elevation,
        )

    async def _show_config_form(
        self, name=None, latitude=None, longitude=None, elevation=None
    ):
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(core.Const.CONF_NAME, default=name): str,
                    vol.Required(
                        core.Const.CONF_LATITUDE, default=latitude
                    ): _cv.latitude,
                    vol.Required(
                        core.Const.CONF_LONGITUDE, default=longitude
                    ): _cv.longitude,
                    vol.Required(core.Const.CONF_ELEVATION, default=elevation): int,
                }
            ),
            errors=self._errors,
        )

    async def async_step_onboarding(self, _data=None):
        """Handle a flow initialized by onboarding."""
        # Don't create entry if latitude or longitude isn't set.
        # Also, filters out our onboarding default location.
        if (not self._shc.config.latitude and not self._shc.config.longitude) or (
            self._shc.config.latitude == Const.DEFAULT_HOME_LATITUDE
            and self._shc.config.longitude == Const.DEFAULT_HOME_LONGITUDE
        ):
            return self.async_abort(reason="no_home")

        return self.async_create_entry(
            title=Const.HOME_LOCATION_NAME, data={Const.CONF_TRACK_HOME: True}
        )


@core.callback
def _configured_instances(comp: core.SmartHomeControllerComponent):
    """Return a set of configured SimpliSafe instances."""
    entries = []
    for entry in comp.controller.config_entries.async_entries(comp.domain):
        if entry.data.get("track_home"):
            entries.append("home")
            continue
        entries.append(
            f"{entry.data.get(core.Const.CONF_LATITUDE)}-"
            + f"{entry.data.get(core.Const.CONF_LONGITUDE)}"
        )
    return set(entries)
