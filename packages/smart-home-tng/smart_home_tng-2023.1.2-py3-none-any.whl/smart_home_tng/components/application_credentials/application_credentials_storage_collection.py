"""
Application Credentials Integration for Smart Home - The Next Generation.

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

from ... import core
from .const import Const


if not typing.TYPE_CHECKING:

    class ApplicationCredentials:
        ...


if typing.TYPE_CHECKING:
    from .application_credentials import ApplicationCredentials


# pylint: disable=unused-variable
class ApplicationCredentialsStorageCollection(core.StorageCollection):
    """Application credential collection stored in storage."""

    def __init__(
        self,
        owner: ApplicationCredentials,
        store: core.Store,
        logger: logging.Logger,
        id_manager: core.IDManager = None,
    ) -> None:
        super().__init__(store, logger, id_manager)
        self._owner = owner

    async def _process_create_data(self, data: dict[str, str]) -> dict[str, str]:
        """Validate the config is valid."""
        result = Const.CREATE_SCHEMA(data)
        domain = result[core.Const.CONF_DOMAIN]
        # pylint: disable=protected-access
        if not await self._owner._get_platform(domain):
            raise ValueError(f"No application_credentials platform for {domain}")
        return result

    @core.callback
    def _get_suggested_id(self, info: dict[str, str]) -> str:
        """Suggest an ID based on the config."""
        return f"{info[core.Const.CONF_DOMAIN]}.{info[core.Const.CONF_CLIENT_ID]}"

    async def _update_data(
        self, data: dict[str, str], update_data: dict[str, str]
    ) -> dict[str, str]:
        """Return a new updated data object."""
        raise ValueError("Updates not supported")

    async def async_delete_item(self, item_id: str) -> None:
        """Delete item, verifying credential is not in use."""
        if item_id not in self._data:
            raise core.ItemNotFound(item_id)

        # Cannot delete a credential currently in use by a ConfigEntry
        current = self._data[item_id]
        entries = self._shc.config_entries.async_entries(
            current[core.Const.CONF_DOMAIN]
        )
        for entry in entries:
            if entry.data.get("auth_implementation") == item_id:
                raise core.SmartHomeControllerError(
                    f"Cannot delete credential in use by integration {entry.domain}"
                )

        await super().async_delete_item(item_id)

    async def async_import_item(self, info: dict[str, str]) -> None:
        """Import an yaml credential if it does not already exist."""
        suggested_id = self._get_suggested_id(info)
        if self._id_manager.has_id(core.helpers.slugify(suggested_id)):
            return
        await self.async_create_item(info)

    def async_client_credentials(self, domain: str) -> dict[str, core.ClientCredential]:
        """Return ClientCredentials in storage for the specified domain."""
        credentials = {}
        for item in self.async_items():
            if item[core.Const.CONF_DOMAIN] != domain:
                continue
            auth_domain = (
                item[Const.CONF_AUTH_DOMAIN]
                if Const.CONF_AUTH_DOMAIN in item
                else item[core.Const.CONF_ID]
            )
            credentials[auth_domain] = core.ClientCredential(
                client_id=item[core.Const.CONF_CLIENT_ID],
                client_secret=item[core.Const.CONF_CLIENT_SECRET],
                name=item.get(core.Const.CONF_NAME),
            )
        return credentials
