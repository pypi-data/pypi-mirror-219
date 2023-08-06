"""
Dashboards Component for Smart Home - The Next Generation.

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

import logging
import typing

import voluptuous as vol

from ... import core
from .const import Const

_LOGGER: typing.Final = logging.getLogger(__name__)

_CREATE_SCHEMA: typing.Final = vol.Schema(Const.STORAGE_DASHBOARD_CREATE_FIELDS)
_UPDATE_SCHEMA: typing.Final = vol.Schema(Const.STORAGE_DASHBOARD_UPDATE_FIELDS)


# pylint: disable=unused-variable
class DashboardsCollection(core.StorageCollection):
    """Collection of dashboards."""

    def __init__(
        self, shc: core.SmartHomeController, storage_key: str, storage_version: int = 1
    ):
        """Initialize the dashboards collection."""
        super().__init__(
            core.Store(shc, storage_version, storage_key),
            _LOGGER,
        )

    async def _async_load_data(self) -> dict:
        """Load the data."""
        if (data := await self._store.async_load()) is None:
            return None

        updated = False

        for item in data["items"] or []:
            if "-" not in item[Const.CONF_URL_PATH]:
                updated = True
                item[Const.CONF_URL_PATH] = f"lovelace-{item[Const.CONF_URL_PATH]}"

        if updated:
            await self._store.async_save(data)

        return typing.cast(typing.Optional[dict], data)

    async def _process_create_data(self, data: dict) -> dict:
        """Validate the config is valid."""
        if "-" not in data[Const.CONF_URL_PATH]:
            raise vol.Invalid("Url path needs to contain a hyphen (-)")

        frontend = self._shc.components.frontend
        if isinstance(frontend, core.FrontendComponent):
            if frontend.is_panel_registered(data[Const.CONF_URL_PATH]):
                raise vol.Invalid("Panel url path needs to be unique")
        else:
            raise vol.Invalid("Frontend Integration not found.")

        return _CREATE_SCHEMA(data)

    @core.callback
    def _get_suggested_id(self, info: dict) -> str:
        """Suggest an ID based on the config."""
        return info[Const.CONF_URL_PATH]

    async def _update_data(self, data: dict, update_data: dict) -> dict:
        """Return a new updated data object."""
        update_data = _UPDATE_SCHEMA(update_data)
        updated = {**data, **update_data}

        if core.Const.CONF_ICON in updated and updated[core.Const.CONF_ICON] is None:
            updated.pop(core.Const.CONF_ICON)

        return updated
