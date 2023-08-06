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

import voluptuous as vol
import voluptuous.humanize as vh

from .callback import callback
from .item_not_found import ItemNotFound
from .storage_collection import StorageCollection
from .web_socket import WebSocket


# pylint: disable=unused-variable
class StorageCollectionWebSocket:
    """Class to expose storage collection management over websocket."""

    def __init__(
        self,
        storage_collection: StorageCollection,
        api_prefix: str,
        model_name: str,
        create_schema: dict,
        update_schema: dict,
    ) -> None:
        """Initialize a websocket CRUD."""
        self._storage_collection = storage_collection
        self._api_prefix = api_prefix
        self._model_name = model_name
        self._create_schema = create_schema
        self._update_schema = update_schema

        assert self._api_prefix[-1] != "/", "API prefix should not end in /"

    @property
    def _shc(self):
        # pylint: disable=protected-access
        return self._storage_collection._shc

    @property
    def item_id_key(self) -> str:
        """Return item ID key."""
        return f"{self._model_name}_id"

    @callback
    def async_setup(
        self,
        *,
        create_list: bool = True,
        create_create: bool = True,
    ) -> None:
        """Set up the websocket commands."""
        comp = self._shc.components.websocket_api
        if not isinstance(comp, WebSocket.Component):
            return

        if create_list:
            comp.register_command(
                f"{self._api_prefix}/list",
                {vol.Required("type"): f"{self._api_prefix}/list"},
                self._list_item,
            )

        if create_create:
            comp.register_command(
                f"{self._api_prefix}/create",
                {
                    **self._create_schema,
                    vol.Required("type"): f"{self._api_prefix}/create",
                },
                self._create_item,
            )

        comp.register_command(
            f"{self._api_prefix}/update",
            {
                **self._update_schema,
                vol.Required("type"): f"{self._api_prefix}/update",
                vol.Required(self.item_id_key): str,
            },
            self._update_item,
        )

        comp.register_command(
            f"{self._api_prefix}/delete",
            {
                vol.Required("type"): f"{self._api_prefix}/delete",
                vol.Required(self.item_id_key): str,
            },
            self._delete_item,
        )

    def _list_item(
        self,
        connection: WebSocket.Connection,
        msg: dict,
    ) -> None:
        """List items."""
        connection.send_result(msg["id"], self._storage_collection.async_items())

    async def _create_item(
        self,
        connection: WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Create a item."""
        connection.require_admin()

        try:
            data = dict(msg)
            data.pop("id")
            data.pop("type")
            item = await self._storage_collection.async_create_item(data)
            connection.send_result(msg["id"], item)
        except vol.Invalid as err:
            connection.send_error(
                msg["id"],
                WebSocket.ERR_INVALID_FORMAT,
                vh.humanize_error(data, err),
            )
        except ValueError as err:
            connection.send_error(msg["id"], WebSocket.ERR_INVALID_FORMAT, str(err))

    async def _update_item(
        self,
        connection: WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Update a item."""
        connection.require_admin()

        data = dict(msg)
        msg_id = data.pop("id")
        item_id = data.pop(self.item_id_key)
        data.pop("type")

        try:
            item = await self._storage_collection.async_update_item(item_id, data)
            connection.send_result(msg_id, item)
        except ItemNotFound:
            connection.send_error(
                msg["id"],
                WebSocket.ERR_NOT_FOUND,
                f"Unable to find {self.item_id_key} {item_id}",
            )
        except vol.Invalid as err:
            connection.send_error(
                msg["id"],
                WebSocket.ERR_INVALID_FORMAT,
                vh.humanize_error(data, err),
            )
        except ValueError as err:
            connection.send_error(msg_id, WebSocket.ERR_INVALID_FORMAT, str(err))

    async def _delete_item(
        self,
        connection: WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Delete a item."""
        connection.require_admin()

        try:
            await self._storage_collection.async_delete_item(msg[self.item_id_key])
        except ItemNotFound:
            connection.send_error(
                msg["id"],
                WebSocket.ERR_NOT_FOUND,
                f"Unable to find {self.item_id_key} {msg[self.item_id_key]}",
            )

        connection.send_result(msg["id"])
