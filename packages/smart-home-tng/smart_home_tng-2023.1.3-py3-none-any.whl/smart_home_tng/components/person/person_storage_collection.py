"""
Person Tracking Component for Smart Home - The Next Generation.

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

_CREATE_SCHEMA: typing.Final = vol.Schema(Const.CREATE_FIELDS)
_UPDATE_SCHEMA: typing.Final = vol.Schema(Const.UPDATE_FIELDS)


# pylint: disable=unused-variable
class PersonStorageCollection(core.StorageCollection):
    """Person collection stored in storage."""

    def __init__(
        self,
        store: core.Store,
        logger: logging.Logger,
        id_manager: core.IDManager,
        yaml_collection: core.YamlCollection,
    ) -> None:
        """Initialize a person storage collection."""
        super().__init__(store, logger, id_manager)
        self._yaml_collection = yaml_collection

    async def _async_load_data(self) -> dict:
        """Load the data.

        A past bug caused onboarding to create invalid person objects.
        This patches it up.
        """
        data = await super()._async_load_data()

        if data is None:
            return data

        for person in data["items"]:
            if person[Const.CONF_DEVICE_TRACKERS] is None:
                person[Const.CONF_DEVICE_TRACKERS] = []

        return data

    async def async_load(self) -> None:
        """Load the Storage collection."""
        await super().async_load()
        self._shc.bus.async_listen(
            core.Const.EVENT_ENTITY_REGISTRY_UPDATED, self._entity_registry_updated
        )

    async def _entity_registry_updated(self, event) -> None:
        """Handle entity registry updated."""
        if event.data["action"] != "remove":
            return

        entity_id = event.data[core.Const.ATTR_ENTITY_ID]

        if core.helpers.split_entity_id(entity_id)[0] != "device_tracker":
            return

        for person in list(self._data.values()):
            if entity_id not in person[Const.CONF_DEVICE_TRACKERS]:
                continue

            await self.async_update_item(
                person[core.Const.CONF_ID],
                {
                    Const.CONF_DEVICE_TRACKERS: [
                        devt
                        for devt in person[Const.CONF_DEVICE_TRACKERS]
                        if devt != entity_id
                    ]
                },
            )

    async def _process_create_data(self, data: dict) -> dict:
        """Validate the config is valid."""
        data = _CREATE_SCHEMA(data)

        if (user_id := data.get(Const.CONF_USER_ID)) is not None:
            await self._validate_user_id(user_id)

        return data

    @core.callback
    def _get_suggested_id(self, info: dict) -> str:
        """Suggest an ID based on the config."""
        return info[core.Const.CONF_NAME]

    async def _update_data(self, data: dict, update_data: dict) -> dict:
        """Return a new updated data object."""
        update_data = _UPDATE_SCHEMA(update_data)

        user_id = update_data.get(Const.CONF_USER_ID)

        if user_id is not None and user_id != data.get(Const.CONF_USER_ID):
            await self._validate_user_id(user_id)

        return {**data, **update_data}

    async def _validate_user_id(self, user_id):
        """Validate the used user_id."""
        if await self._shc.auth.async_get_user(user_id) is None:
            raise ValueError("User does not exist")

        for persons in (self._data.values(), self._yaml_collection.async_items()):
            if any(
                person
                for person in persons
                if person.get(Const.CONF_USER_ID) == user_id
            ):
                raise ValueError("User already taken")
