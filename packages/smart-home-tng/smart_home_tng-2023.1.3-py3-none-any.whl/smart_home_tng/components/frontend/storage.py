"""
Frontend Component for Smart Home - The Next Generation.

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

import collections.abc
import typing

import voluptuous as vol

from ... import core

_SET_DATA: typing.Final = {
    vol.Required("type"): "frontend/set_user_data",
    vol.Required("key"): str,
    vol.Required("value"): vol.Any(bool, str, int, float, dict, list, None),
}
_GET_DATA: typing.Final = {
    vol.Required("type"): "frontend/get_user_data",
    vol.Optional("key"): str,
}


# pylint: disable=unused-variable
class Storage:
    """API for persistent storage for the frontend."""

    @staticmethod
    async def async_setup_frontend_storage(api: core.WebSocket.Component) -> None:
        """Set up frontend storage."""
        api.register_command(_set_user_data, _SET_DATA)
        api.register_command(_get_user_data, _GET_DATA)


async def _with_store(
    func: collections.abc.Callable[
        [
            core.WebSocket.Connection,
            dict,
            core.Store,
            dict | list,
        ],
        collections.abc.Awaitable,
    ],
    connection: core.WebSocket.Connection,
    msg: dict,
):
    """Provide user specific data and store to function."""
    user_id = connection.user.id

    store = core.Store(
        connection.owner.controller,
        1,
        f"frontend.user_data_{user_id}",
    )

    data = await store.async_load() or {}
    return await func(connection, msg, store, data)


async def _get_user_data(connection: core.WebSocket.Connection, msg: dict):
    await _with_store(_internal_get_user_data, connection, msg)


async def _internal_get_user_data(
    connection: core.WebSocket.Connection,
    msg: dict,
    _store: core.Store,
    data: dict[str, typing.Any],
) -> None:
    """Handle get global data command.

    Async friendly.
    """
    connection.send_result(
        msg["id"], {"value": data.get(msg["key"]) if "key" in msg else data}
    )


async def _set_user_data(connection: core.WebSocket.Connection, msg: dict):
    await _with_store(_internal_set_user_data, connection, msg)


async def _internal_set_user_data(
    connection: core.WebSocket.Connection,
    msg: dict,
    store: core.Store,
    data: dict[str, typing.Any],
) -> None:
    """Handle set global data command.

    Async friendly.
    """
    data[msg["key"]] = msg["value"]
    await store.async_save(data)
    connection.send_result(msg["id"])
